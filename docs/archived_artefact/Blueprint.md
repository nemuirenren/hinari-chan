# Hinari — Low-Level Blueprint (v1)

> Status: blueprint. Abstraction and pipeline refer to the locked LLD.
> LLD: `docs/Low-Level Design.md` (duplicate: `docs/hinari-low-level-design.md`).
> Executable pseudocode (source of truth): `tests/test_pipeline.py` (`demo()` passes).
> 13-node visual pipeline: `docs/pipeline.png`.
> Role mechanics: `docs/research/chat-completions-role-mechanics-report.md`, `docs/research/chat-completions-role-mechanics-evidence.md`.
> Local Discord API notes (not an agent framework): `docs/discord/01-api.md`, `02-interactions-api.md`, `03-ext-commands-commands.md`, `04-ext-tasks-index.md`.

This document is the **locked owner intent** plus the laziest technical derivation that still satisfies the five owner requirements:
1. easy to extend, 2. easy to fix, 3. easy to locate bugs, 4. isolated blast radius, 5. well-organized source.

Ponytail still applies to **how** it is implemented, never to **what** was requested.

---

## 1. Owner intent (locked, not subject to YAGNI)

1. Hinari is a Discord bot, active in **exactly 1 server and 1 channel**. Anything outside is ignored early.
2. One human-like agent in one group chat. Exactly one agent: **Hinari**. Selectivity, delay, silence, and initiative come from harness structure, not prompting. No assistant-bot behavior.
3. **No AI agent framework** (no LangChain / LangGraph / etc).
4. Dependencies via `uv add <dependency>` **without pinned versions** → today's versions become the locked versions. `pyproject.toml` is required.
5. Run with a single command: `uv run hinari`.
6. Later (out of scope for now, but this blueprint reserves the contract): `startup.sh` (runs `uv run hinari` and auto-creates a `.service` file for 24/7 operation) and `reset.sh` (factory reset).
7. Exactly **one** LLM parameter: `temperature: 1`. No `max_tokens`, no `top_p`, nothing else.
8. Logging must go to `log.txt` (in addition to console).
9. On every `uv run hinari` boot, a dedicated **startup compatibility check** verifies behaviorally whether the configured AI model is compatible with Hinari. A reference model known by the owner to be 100% functional is FYI only: it **must not** be used as a default and **must not** appear anywhere in source, config, docs, tests, or logs. The model comes purely from user env; pass/fail comes purely from probes.
10. Agreed LLD clarification: **any generated `assistant` message after the payload (not the pinned LORE sitting with `system`) with no `tool_calls` is fully ignored**, whether or not it carries `content`. Already specified in LLD §2 (roles table), §5 (`NORMALIZE` + `MISS_HANDLER`), §8 (invariants 3–4), and `demo()` in `tests/test_pipeline.py` (`normalize` + `handle_miss`). History appends only real `tool_calls` plus real `tool` results (Law 3).
11. The `tests/` folder is left to the implementor: any number of files, any methods (compile, smoke, etc). Single goal: **100% fully functional**.

Non-goals for v0 (from LLD, still binding): multi-room, moderation tooling, scheduler daemons, vector recall, sentiment classifiers, group voice calls, payments. Blueprint additions: slash commands / interactions, `ext.commands` prefix bot, DB server, queue, Docker.

---

## 2. Architecture: modular monolith, pure core + thin adapters

Type: **single-process modular monolith, lite ports-and-adapters**.

```
                    ┌─────────────────────┐
                    │   Discord Gateway   │
                    │  (1 guild, 1 ch)    │
                    └────────┬────────────┘
                             │ on_message → buffer only + guard
                             ▼
                    ┌─────────────────────┐
                    │ adapters/           │
                    │ discord_phone.py    │  read_chat(7)/scroll(7)/search/pick(11)/
                    │ + 1srv/1ch guard    │  send_message + typing delay
                    └────────┬────────────┘
                             ▼
┌──────────────┐   ┌─────────────────────┐   ┌──────────────┐
│ prompts/     │──▶│ harness/            │──▶│ adapters/    │
│ SYSTEM/IDENT │   │ pipeline.py (13     │   │ llm.py       │
│ LORE/moods/  │   │ nodes) + state.py   │   │ stdlib urllib│
│ relationships│   │ TRIGGER→APPEND      │   │ temp=1 only  │
└──────────────┘   └────────┬────────────┘   └──────────────┘
                            │                    ▲
                            ▼                    │
                    ┌─────────────────────┐      │
                    │ adapters/store.py   │──────┘
                    │ JSON atomic, 1KB,   │
                    │ [[link]] check      │
                    └─────────────────────┘
```

One-way dependency rule (no leakage):

* `harness/` **never imports** `discord`, network, env, or files.
* `adapters/*` may import `harness/` plus stdlib (`discord.py` only inside `discord_phone.py`).
* `main.py` + `config.py` are wiring only: env → `log.txt` → compat check → Discord connect → TRIGGER loop.
* Errors are never swallowed. Each layer adds its module context so a traceback points at the area (traceability + blast radius).

Why not the alternatives:

* Not `commands.Bot` / slash / interactions: Hinari is a member, not a command bot. Per `docs/discord/`, `discord.Client + on_message + ext.tasks.loop` suffices (tasks ships with `discord.py`, no new dependency).
* Not full layered / hexagonal: overkill for 6 tools and 1 channel. One core plus three adapters is enough.
* Not microservices / queue / DB: LLD §4(6) + §6 (harness-computed state + 1KB files) already covers it. A DB would be YAGNI.

---

## 3. Folder and file layout (to be created later, not now)

```
hinari/
├─ pyproject.toml            # [project.scripts] hinari = "hinari.main:main", dep: discord.py
├─ .env.example              # DISCORD_TOKEN/GUILD_ID/CHANNEL_ID/LLM_* (no values)
├─ startup.sh                # FUTURE: uv run hinari + write .service (not built yet)
├─ reset.sh                  # FUTURE: rm -rf state/ (not built yet)
├─ log.txt                   # runtime, gitignored (like .env, state/)
├─ hinari/ (flat package: hatchling default, no extra build config)
│  ├─ __init__.py
│  ├─ main.py                # `uv run hinari` entry: env → log → compat check → discord → TRIGGER loop
│  ├─ config.py              # stdlib env load, LLD constants, 1srv/1ch IDs
│  ├─ compat.py              # behavioral startup compat check, no model names
│  ├─ harness/
│  │  ├─ __init__.py
│  │  ├─ state.py            # State dataclass + stamina/mood/relationship math (LLD §6)
│  │  └─ pipeline.py         # TRIGGER, RENDER_SYSTEM, PINNED_LORE, NORMALIZE,
│  │                         # MISS_HANDLER, DISPATCH (6 tools), UPDATE_STATE,
│  │                         # SLIDE_WINDOW, APPEND, SLEEP_PATH
│  └─ adapters/
│     ├─ __init__.py
│     ├─ discord_phone.py    # phone implementation via discord.py + guard + \n\n split
│     ├─ llm.py              # CALL_LLM via urllib, temp=1, [DONE]-strip, reasoning-strip
│     └─ store.py            # memories/history/mood/relationship persistence, atomic, 1KB cap
├─ prompts/                  # owner-editable, not code
│  ├─ SYSTEM.md  IDENTITY.md  LORE.md
│  ├─ moods/mapping.yaml + 11 *.md
│  └─ relationships/mapping.yaml + 13 *.md
├─ state/                    # runtime JSON, gitignored, reset.sh target
├─ tests/
│  ├─ test_pipeline.py       # LOCKED source of truth, do not casually change
│  ├─ test_harness.py        # FUTURE (see §11)
│  ├─ test_adapters.py       # FUTURE
│  ├─ test_startup.py        # FUTURE
│  └─ test_smoke.py          # FUTURE
└─ docs/
   ├─ Low-Level Design.md / hinari-low-level-design.md (locked)
   ├─ Blueprint.md (this document)
   ├─ pipeline.png (13 nodes)
   ├─ research/ + discord/
```

File contracts (rough):

* `config.py`: the only env reader plus constants (`7/7/5/11`, burst `20`, curfew `01:00`, budget `100000`, `500/1KB/20 pairs`). Missing env → clear error + exit before network.
* `main.py`: strict order `load config → init log.txt → compat check → Discord connect → TRIGGER loop`. No hidden args.
* `compat.py`: behavioral probes (see §8). No discord import. Pass → return; fail → cause to `log.txt` + stderr + `sys.exit(2)` with a "change MODEL" message.
* `harness/state.py`: pure stamina/mood/relationship functions. The model never writes them directly (LLD §6).
* `harness/pipeline.py`: the 13 nodes with exactly the LLD + `pipeline.png` names. No knowledge of Discord/HTTP/files.
* `adapters/discord_phone.py`: the only file importing `discord`. Top guard: wrong `guild_id`/`channel_id`/bot-self author → return. `on_message` only appends a buffer plus `mentioned/unread` flags; it never calls the LLM directly.
* `adapters/llm.py`: the only HTTP file. Sends `temperature: 1` only. Tolerant parsing (trailer strip), drops `reasoning`, validates `tool_calls[].function.arguments` JSON, falls back `tool_choice required → auto`.
* `adapters/store.py`: the only `state/` writer. Atomic (`tmp + rename`), rejects `>1024 bytes`, prepends time+date, stdlib `[[link]]` scan → `{written, broken}`.
* `prompts/*`, `state/*`: see §7 + §10.

---

## 4. Runtime flows

### 4.1 Boot (`uv run hinari`) — mandatory order

```
env/config → init log.txt → compat check (no Discord yet)
  ├─ FAIL → log + stderr "change MODEL" + exit 2 (never connects to Discord)
  └─ PASS → Discord connect → tasks.loop(TRIGGER) runs → idle
```

### 4.2 Message ingest (never wakes the LLM directly)

```
on_message:
  if guild.id != GUILD_ID or channel.id != CHANNEL_ID → return
  if author.bot or author == self → return
  append {from, time, text} to group buffer
  unread += 1; if @hinari in text → mentioned = True
```

### 4.3 Wake + tool loop (exactly LLD §5; one frozen `sys` snapshot per wake)

```
reason = TRIGGER()  # until | @mention/burst>=20 | stamina<=0 | >=01:00
if None → stay asleep, zero requests
sys = RENDER_SYSTEM()   # SYSTEM.md + {identity}, counts/flags only
lore = PINNED_LORE()    # LORE.md verbatim at index 1
misses = 0
loop:
  msg = CALL_LLM(sys + lore + history_tail, temperature=1, tool_choice=required|auto)
  msg = NORMALIZE(msg)  # content → null except lore; keep tool_calls only
  if empty → MISS_HANDLER: retry once on same sys; twice → sleep 5min, append nothing, break
  for call in tool_calls:
    res = DISPATCH(call)       # phone/body/memory
    UPDATE_STATE(call, res)    # stamina/mood/relationship
    SLIDE_WINDOW()             # keep 0–1, drop whole oldest pairs, protect 20
    APPEND(calls + res)        # real events only
    if do_activity → break to outer sleep
```

### 4.4 Sleep / shutdown / ops

* `do_activity(label, until)` → freeze with zero requests until `until`. Wake report `{woke_at, elapsed, unread_delta}`.
* `stamina <= 0` forces sleep until 500; `>= 01:00` forces sleep until 500. No model veto.
* Shutdown (SIGTERM from `.service`): atomic `store.py` flush, Discord close, one line to `log.txt`.
* Future `reset.sh`: only `rm -rf state/ log.txt`. `prompts/` and `.env` are untouched, so factory reset restores factory-empty relationship/mood/memory while keeping owner character files.

---

## 5. System sheet + LORE (rendered, not generated)

Template (LLD §3, no `<reality>` block):

```
<identity>  {identity} verbatim from IDENTITY.md </identity>
<time>      weekday, YYYY-MM-DD, HH:MM + tz </time>
<activity>  label until until; phone silent, mention-vibration on </activity>
<group>     members; unread=N mentioned=bool; full text NOT shown </group>
<memory>    own-note tail ≤5 lines. No file list. </memory>
<mood>      1 paragraph from the active moods/<score>.md </mood>
```

* Member text is never pasted into `system` (trust boundary). Full text requires an explicit `read_chat` / `scroll` / `search` call.
* `assistant` at index 1 is `LORE.md` verbatim, no char limit, never slides (§7), never normalized (§5). Voice quirks live there plus in `send_message` args.

---

## 6. Tools (6, mapped to Discord + files)

| # | LLD tool | Adapter | Contract |
|---|---|---|---|
| 1 | `read_chat()` | `discord_phone` | 7 newest bubbles. Entry point, no args. Each bubble annotated `{from, time, text, rel}` |
| 2 | `scroll_chat(offset)` | `discord_phone` | 7 bubbles from offset `7, 14, …` from newest |
| 3 | `search_chat(query)` / `(query, pick)` | `discord_phone` | ≤5 hits `{id, time, from, snippet}` with no context; with `pick` → 11 bubbles (5 + picked as #6 + 5), positional jump |
| 4 | `send_message(text)` | `discord_phone` | One string; `\n\n` splits into bubbles; harness derives typing delay from length, the model never computes speed; returns `{delivered}` |
| 5 | `do_activity(label, until)` | `harness` + loop | Freeze with zero requests; returns `{sleeping_until}` |
| 6 | `memory(list/read/write)` | `store` | One global namespace, sorted `list`, `read` ≤1KB, `write` rejects `>1024B`, prepends time+date, plain-text `[[link]]` stdlib scan → `{written, broken}` |

`rel` is `"<Type> (<score>): <one-line>"` from the sender's current relationship band.

---

## 7. Harness state math + window (computed, never model-written)

* Stamina max 500: `drain = 0.15 * exp(hours_awake / 6)`, `cost = duration * multiplier * 0.5`, `recovery = +1.2/min` (~500 per 7h). All-nighters collapse on their own (0→12h ≈ −345).
* Mood 0–10 (`Ecstatic … Devastated`), one file per level with `name/score/category` frontmatter. `target = clamp(5 + stamina_part + activity_part + social_part)`, `new = round(0.7 * old + 0.3 * target)`. Glides, never teleports.
* Relationship −500…+500, 13 bands, factory-empty → Neutral on first appearance. Structural signals only (reply / initiate / ignored mention), no sentiment model. `gain ≤ +3/day (replied ≥1x and mood ≥ 6)`, `loss ≤ −5/day (mention ignored past next wake or mood ≤ 3)`, `decay 0.2/day after 3 idle days`. 0→500 takes ≈167 days. Loss outruns gain.
* 100000-token window (deployment's real tokenizer). Pin indices 0–1. Drop oldest whole pairs, never half a pair (id pairing breaks), never drop newest 20. An oversized single read is rejected and retried with a smaller offset instead of mid-truncation.

Owner-editable: `SYSTEM.md`, `IDENTITY.md`, `LORE.md`, `relationships/mapping.yaml + 13 md`, `moods/mapping.yaml + 11 md`, activity multiplier + pleasantness tables, `7/7/5/11`, burst `20`, mention rule, `01:00` curfew.

---

## 8. Startup compatibility check (behavioral, no model names in code)

Ban: the owner's reference model string **must not** appear in source, config, docs, tests, or logs. The check is behavioral, never `if model == ...`.

Minimal probes (stdlib, `temperature: 1`, no `max_tokens` / `top_p`), before Discord connects:

1. Basic call → must return `finish_reason = tool_calls` plus valid-JSON `arguments` and the right tool name.
2. Closed loop → echo a string `tool` result with exact `tool_call_id` back → must return `stop` with no spurious calls, and the final content must use that data.
3. Provider robustness (from research F2/F4): tolerate a `data: [DONE]` trailer, enforce our own validation that `tool` without `tool_call_id` fails, and require string `tool.content`.

All pass → continue. Any fail → write which probe plus a short body to `log.txt` + stderr, exit `2` with "change MODEL and rerun `uv run hinari`". No network auto-retry, no silent model fallback.

```
uv run hinari → compat FAIL → [log.txt] compat=FAIL probe=basic_call reason=no-tool_calls
                → stderr: "Model incompatible. Change MODEL and rerun."
                → exit 2 (Discord never connects)
```

---

## 9. LLM contract (the only HTTP place)

* Transport: stdlib `urllib` (as in the research harness), JSON strings for `tool.content`, exact `tool_call_id` pairing.
* Payload fields only: `model, messages, tools, tool_choice, temperature: 1`. **Forbidden**: `max_tokens`, `top_p`, `frequency_penalty`, etc.
* `messages`: `[system(rendered), assistant(LORE verbatim), ...history_tail(assistant null + tool_calls / tool)]`. **No `user` role.**
* `tool_choice`: `required` where supported, else `auto` plus the same miss handler (LLD §5).
* Response hygiene: strip `\s*data:\s*\[DONE\]\s*$`, drop `reasoning` / `reasoning_details` from user-facing output, `content or ""`, validate `arguments` JSON before dispatch. A provider ignoring `tool_choice: none` is normal behavior (E1.5), not an error.
* All guarantees live in the harness (Law 4). The model may misbehave; `NORMALIZE + MISS_HANDLER + SLIDE + APPEND` enforces correctness.

---

## 10. Discord mapping + persistence

* Library: `discord.py` only (see `docs/discord/`). `discord.Client`, not `commands.Bot`. No prefix commands, no slash. Intents: `guilds + messages + message_content` (`message_content` must also be enabled in the portal). No `members` / `presences` (unneeded for 1 channel).
* `ext.tasks.loop` only ticks `TRIGGER` (mention / burst / until / stamina / curfew). Not a feature scheduler daemon (non-goal).
* 1-server / 1-channel guard in two layers: `config` (IDs required) plus the first line of `on_message` / fetch (mismatch → return). A wrong server/channel is not an error, just ignored plus one debug log line.
* `send_message`: split on `\n\n`, send sequentially, harness-computed typing delay from length.
* Persistence: `state/*.json` (history tail, stamina/mood/relationship, memories, clock). Atomic writes. `prompts/` is never written by the bot. `reset.sh` deletes `state/` + `log.txt` only.

`.gitignore` must cover: `.venv/ __pycache__/ *.pyc .env state/ log.txt`.

---

## 11. Tests: what + how (goal: fully functional, no network)

Principle: stdlib `unittest` + `compileall`, no `pytest`. Skipped: pytest / coverage / mock libs — add only if blocked. No tokens, no internet; LLM and Discord are always faked.

| File | Method | What it proves (failure = that area is broken) |
|---|---|---|
| `test_pipeline.py` (locked) | `demo()` asserts | 13 nodes + 7 LLD §8 invariants |
| `test_harness.py` | Pure unit | TRIGGER reasons, NORMALIZE → null, MISS retry-once → sleep-5min append-nothing, 7/7/5→11 (#6) pages, 1KB memory + broken links, stamina/mood/relationship math, SLIDE pin 0–1 + whole pairs + protect 20, real-only APPEND |
| `test_adapters.py` | Contract + fakes | Wrong guild/channel guard, `\n\n` split, payload shape with only `temperature: 1`, tool schema, `[DONE]`-strip, reasoning-strip, `required → auto` fallback, atomic store + 1KB + `[[link]]` |
| `test_startup.py` | Mock matrix | Compat PASS (basic + loop + robustness) → continue; each FAIL → exit 2 + change-MODEL message, Discord never connects; asserts no model-name strings in code |
| `test_smoke.py` | Compile + dry wiring | `compileall src/`, import `main` with no network, missing env → clear error, dry boot creates `log.txt` |

Fully functional here means: all asserts green plus one dry wake → tool-loop → sleep cycle with fake Discord + fake LLM green plus `uv run hinari` failing clearly on bad env / MODEL.

---

## 12. Ops contract (future, not built yet)

* `pyproject.toml`: `[project.scripts] hinari = "hinari.main:main"`. Dependency: `discord.py` only (version locked on execution day via `uv add discord.py`). Everything else stdlib.
* `.env`: `DISCORD_TOKEN, DISCORD_GUILD_ID, DISCORD_CHANNEL_ID, LLM_BASE_URL, LLM_API_KEY, LLM_MODEL`. `LLM_MODEL` is free-form user input; no model default in code.
* `uv run hinari`: the only supported run path.
* Future `startup.sh`: `uv run hinari` plus generated `.service` (`ExecStart=uv run hinari`, `Restart=always`, env from file, logs to `log.txt` + journal). Idempotent.
* Future `reset.sh`: stop service (if present) + `rm -rf state/ log.txt` + exit 0. Never touches `prompts/` / `.env`.
* `log.txt`: stdlib logging, default `INFO`, format `time level module: message`, same content on console and file. Every error logs module + probe/tool + short IDs (never tokens).

---

## 13. Locked constants (change only on explicit owner tuning request)

`SCREEN 7`, `SEARCH_HITS 5`, `SEARCH_WINDOW 11 (picked is #6)`, `PROTECT_LAST 20`, `CTX 100000`, `STAMINA_MAX 500`, `MEM_MAX 1024`, burst `20`, curfew `01:00`, miss `retry 1x → sleep 5min append nothing`, `temperature 1`.

---

## 14. Risks + settled decisions

* Provider quirks (research E1–E8: trailer bug, ignored `tool_choice: none`, unreliable thinking toggles, replica non-determinism, JP bleed) → handled in `llm.py` plus the miss handler, not in prompts.
* State conflicts (Law 3 / E7: blend, not override) → resolved in the store plus sheet re-render, never by contradicting history. Forgetting means cut / compact, not overwriting narrative.
* Persona is output-side only (E6.4) → character in LORE plus curated history; authoritative facts in tools / state.
* Probabilistic adoption (battery 20% vs. earthquake 2/2 plus hoax reversal) → critical facts must be short, imperative, coherent, or go through the system sheet / code outside the model.

---

## 15. Traceability

`LLD §§1–10 → Blueprint §§1–15 → (later) hinari/* + tests/test_*.py`.
Pipeline node names in code must match `pipeline.png` plus LLD §5. Every LLD §8 invariant must have an assert in `tests/`. Every §1 intent must map to the file implementing it, with no orphan files.
