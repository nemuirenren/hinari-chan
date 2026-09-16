# Hinari — Low-Level Design (v1, Locked)

Single human-like agent in a single group chat. One agent only: **Hinari**.
No assistant-bot behavior. Selectivity, delay, and initiative come from structure, not prompting.

- Executable pseudocode (source of truth): `tests/test_pipeline.py` (`demo()` passes).
- Visual pipeline: `docs/result/pipeline.png` (13 nodes, same names as §5).
- Role mechanics background: `docs/research/chat-completions-role-mechanics-report.md`, `docs/research/chat-completions-role-mechanics-evidence.md`.

Status: abstraction + pipeline locked. Stack/libraries/packages out of scope.

---

## 1. Goals / Non-goals

Goals:

1. Hinari reads and writes as one member among humans, with human shortcomings: limited screen, truncated notifications, busyness, fatigue.
2. She replies only when she chooses; delay and silence are first-class outcomes.
3. Long-term memory, stamina, mood, and per-person relationship are persistent and owner-editable.
4. Every guarantee lives in the harness loop, never in the model (Law 4 of the role report).

Non-goals (v0): multi-room, moderation tooling, scheduler daemons, vector recall, sentiment classifiers, group voice calls, payment.

## 2. Roles (3 of 4 Chat Completions roles)

| Role | Meaning here | Rules |
|---|---|---|
| `system` | Situation sheet, rebuilt fresh every wake. Facts, not commands. | Harness-rendered only. No raw member text. No memory file list. Short. |
| `assistant` | Hinari's recorded behavior + one pinned exception. | Generated contents always normalized to `null`; only `tool_calls` kept (E1.2). The single pinned `LORE.md` message (§3.1) is verbatim and never normalized. Never sent to the room. |
| `tool` | The world's answer to her action. | JSON-string payloads. Exact id pairing. Untrusted content, trusted provenance. |
| `user` | — | **Never used.** All room text arrives via `tool`. This strips "someone speaking to me" pressure (§6.4) and yields probabilistic adoption for free. |

History invariant: append only real utterances-as-tool-calls plus real results. Never append synthetic turns, never rewrite a `tool_call`, never contradict — cut instead (Law 3).

## 3. System sheet (rendered, not generated)

No second agent generates inner speech. `system` = deterministic template loaded from
owner-editable `SYSTEM.md` with dynamic slots filled per wake. `<identity>` is
`{identity}` loaded verbatim from owner-editable `IDENTITY.md`. No `<reality>` block.

```
<identity>  {identity} — verbatim from IDENTITY.md </identity>
<time>      <weekday, YYYY-MM-DD, HH:MM + tz> </time>
<activity>  <label> until <until>; phone silent, mention-vibration on </activity>
<group>     room members; unread=<N> mentioned=<bool>; full text NOT shown </group>
<memory>    latest own-note tail (≤5 lines). No file list. </memory>
<mood>      1 paragraph from moods/<score>.md </mood>
```

Trust boundary: whoever writes this channel authors reality. Member text is never pasted here — counts and sender flags only. Full text requires an explicit read tool.

### 3.1 Pinned lore (the only surviving assistant content)

One `assistant` message sits immediately after `system` on every request:

- Content = `LORE.md` verbatim, owner-editable free prose (e.g. first-person history), no character limit.
- Position fixed at index 1; never slid out (§7), never normalized (§5).
- It is the curated character anchor (report §6.3: first curated turns outweigh persona paragraphs). Voice quirks live here plus in `send_message` args.

## 4. Tools (6 total)

Phone (room access):

1. `read_chat()` → latest `7` bubbles. Entry point, no args.
2. `scroll_chat(offset)` → `7` older bubbles starting `offset` from newest (`7`, `14`, …). This is scrolling.
3. `search_chat(query)` → ≤`5` hits `{id, time, from, snippet}`. No surrounding context.
   `search_chat(query, pick=id)` → `11` bubbles: 5 before + picked as #6 + 5 after. A positional jump, not a scroll.
4. `send_message(text)` → one string; `\n\n` splits into room bubbles. Harness derives typing delay from length; the model never computes speed. Returns `{delivered: time}`.

Body (time):

5. `do_activity(label, until)` → freeze until `until`. Zero requests while asleep. Returns `{sleeping_until}`.

Long-term memory (obsidian-like, minimal):

6. `memory(op, name, text)` with `op ∈ {list, read, write}`.
   - `list` → sorted filenames. `read(name)` → up to 1 KB text.
   - `write(name, text)` → create/overwrite; harness prepends `time + date` line; rejects body `>1024` bytes.
   - Links are plain `[[name]]` text. Harness scans `[[…]]` against existing files (stdlib) and returns `{written, broken:[…]}`. Repair = ordinary `write` of the missing file or an edit. No graph DB, no daemon.

Read results annotate every bubble: `{from, time, text, rel}` where `rel` = `"<Type> (<score>): <one-line desc>"` from the sender's current relationship band (§6.3). Wake results after `do_activity` report `{woke_at, elapsed, unread_delta}`.

## 5. Pipeline (13 nodes, cf. `docs/result/pipeline.png`)

Pseudocode (condensed; runnable form in `tests/test_pipeline.py`):

```
loop forever:
  reason = TRIGGER()                       # until | @mention/burst | stamina<=0 | >=01:00
  if reason is None: continue sleeping     # no request while asleep
  sys = RENDER_SYSTEM()                    # SYSTEM.md + {identity} from IDENTITY.md
  lore = PINNED_LORE()                     # LORE.md verbatim at index 1
  misses = 0
  loop:                                    # tool loop, same sys+lore snapshot
    msg = CALL_LLM(sys + lore + history_tail, tool_choice=required|auto)
    msg = NORMALIZE(msg)                   # generated content -> null; lore untouched
    if msg.tool_calls is empty:            # MISS_HANDLER
      misses += 1
      if misses == 1: continue             # retry once, same sys
      sleep(5min); append nothing; break   # fail 2x -> idle sleep
    for call in msg.tool_calls:
      res = DISPATCH(call)                 # §4 paths
      UPDATE_STATE(call, res)              # §6 harness math
      SLIDE_WINDOW()                       # §7
      APPEND(msg.tool_calls + res)         # real events only
      if call is do_activity: break to outer sleep
```

- `TRIGGER` sends the only out-of-loop request. In-loop follow-ups reuse the wake's `sys`.
- `NORMALIZE` + `MISS_HANDLER`: content without a call is a miss. Retry once; on second miss sleep 5 min and append nothing (keeps history truthful, guarantees progress).
- `tool_choice=required` where the model supports it, else `auto` + the same miss handler.

## 6. Harness state (computed, never model-editable)

### 6.1 Stamina (max 500)

```
drain_awake_per_min = 0.15 * exp(hours_awake / 6)
activity_cost       = duration_min * label_multiplier * 0.5   # mapping, owner-editable
recovery_while_asleep = +1.2 / min                            # ≈500 per 7 h
stamina             = clamp(stamina - drain - cost + recovery, 0, 500)
```

Enforcement: `stamina <= 0` forces sleep until 500; wall clock `>= 01:00` forces sleep until 500 immediately. No model veto. Awake exponent makes all-nighters collapse on their own: 0→12 h ≈ −345, 0→16 h ≈ −723.

### 6.2 Mood (0–10, English keys, file per level)

Default mapping (owner-editable via `moods/mapping.yaml`):

`10 Ecstatic, 9 Elated, 8 Cheerful, 7 Pleasant, 6 Calm, 5 Flat, 4 Low, 3 Gloomy, 2 Distressed, 1 Miserable, 0 Devastated`

Each level = `moods/<name>.md` with YAML frontmatter (`name, score, category`) + a behavior-guidance body; the body of the current level is injected as the `<mood>` paragraph. Categories are free-form for the owner (e.g. `tired-gloomy`).

Update (harness, momentum — moods glide, never teleport):

```
stamina_part  = 4 * (stamina/500) - 2              # +2 .. -2
activity_part = pleasantness(label)                # -2 .. +2, mapping
social_part   = mean over interacted senders of (rel_score/500) * 2
target        = clamp(5 + stamina_part + activity_part + social_part, 0, 10)
mood_new      = round(0.7 * mood_old + 0.3 * target)
```

### 6.3 Relationship (−500…+500, 13 bands, factory-empty)

No names exist at first run. A name is created as Neutral on first appearance.

| Band | Range |
|---|---|
| Profound Hatred | −500…−400 |
| Hostility | −400…−320 |
| Resentment | −320…−240 |
| Distrust | −240…−160 |
| Discomfort | −160…−80 |
| Aloofness | −80…−20 |
| Neutral | −20…+20 |
| Acquaintance | +20…+80 |
| Cordiality | +80…+160 |
| Warmth | +160…+240 |
| Trust | +240…+320 |
| Deep Affection | +320…+400 |
| Devotion | +400…+500 |

Defined in `relationships/mapping.yaml` (range → file) + 13 `.md` files (one per band, owner-editable). Each person holds one score.

Dynamics (slow by design, structural signals only — replies, initiations, ignored mentions; no sentiment model):

```
gain:  ≤ +3/day if Hinari replied ≥1x and mood ≥ 6
loss:  ≤ −5/day if a mention was ignored past next wake or mood ≤ 3 during contact
decay: score -= sign(score) * 0.2 * days_idle   (after 3 idle days, toward 0)
```

0→500 needs ≈167 consecutive positive days. Loss outruns gain (negativity bias).

### 6.4 Memory files

Covered in §4(6). One global namespace, 1 KB/file cap, timestamp auto-prepended, `[[link]]` + `broken` warnings. Discovery is deliberate: with no file list in `system`, Hinari opens memory only when she chooses `memory(list|read)`.

## 7. Context window (100 000, sliding)

- Budget: 100 000 tokens by the deployment's real tokenizer.
- Pinned: current `system` (index 0, rebuilt) + `LORE.md` assistant message (index 1, verbatim, no char limit, always counted).
- Sliding: generated `assistant(null + tool_calls)` / `tool` pairs after index 1; over budget → drop oldest whole pairs first (never half a pair — id pairing breaks; never index 0–1). Newest 20 pairs are never dropped; an oversized single read is rejected and retried with a smaller offset instead of mid-truncated.

## 8. Invariants (checked by `demo()`)

1. No request while asleep; wake reasons only.
2. `system` = `SYSTEM.md` + `{identity}` from `IDENTITY.md`; no `<reality>`; counts/flags only, never raw member text or a memory file list.
3. Stored `assistant.content` is `null` everywhere except pinned `LORE.md` at index 1.
4. Miss appends nothing; at most one retry, then 5-min idle sleep.
5. Reads are fixed pages (7 / 7 / 5→11-centered); memory writes reject `>1KB` and report `broken` links.
6. Stamina/mood/relationship update in harness; the model never writes them directly.
7. Sliding keeps indices 0–1 and drops whole oldest pairs after them; pairing integrity holds at any budget.

## 9. Owner-editable surface

`SYSTEM.md` (template prose + slots); `IDENTITY.md` (`{identity}` source); `LORE.md` (pinned lore, free prose, no char limit); `relationships/mapping.yaml` + 13 band `.md` files; `moods/mapping.yaml` + 11 mood `.md` files (frontmatter `name/score/category`); activity multipliers + pleasantness table; page sizes (`7/7/5/11`), burst threshold (`20`), mention-vibration rule, `01:00` curfew. Constants stay fixed until tuning is requested.

## 10. Deferred (explicitly not v0)

Real tokenizer wiring, exact typing-speed curve, wall-clock timezone binding, multi-room, moderation, memory summarizer agent (add only when recall demonstrably fails despite the log containing the fact).
