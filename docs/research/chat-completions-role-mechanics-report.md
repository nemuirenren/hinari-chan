# Chat Completions Roles Under a Black-Box Microscope

**An experimental report on what `system`, `user`, `assistant`, and `tool` actually do — evidence from ~80 live requests against one OpenAI-compatible endpoint.**

- **Date:** 14 September 2026
- **Target:** local proxy (`/v1/chat/completions`, 149 registered models)
- **Model under test:** alias `hinari-model` → upstream backend `mimo-v2.5-free` (Xiaomi MiMo v2.5, self-confirmed in its own reasoning output — see E5.3)
- **Method:** black-box probing. Every claim below comes from a request/response pair captured during the session. Where the sample is small (n=1), it is marked as such.
- **Author's note:** this document was assembled from a live interactive experiment session; latency figures are from one machine, one network, one moment. Treat them as anecdote-with-numbers, not benchmarks.

---

## Table of contents

1. [TL;DR — the findings that mattered](#1-tldr)
2. [Environment quirks discovered before anything else](#2-environment)
3. [Experiment log E1–E8 with evidence](#3-experiments)
4. [The universal mechanics of the four roles](#4-mechanics)
5. [Four laws derived from the data](#5-laws)
6. [Design guide: a multi-user, stateful, social agent harness](#6-harness)
7. [Conclusions](#7-conclusions)
8. [Appendix: reproduction payloads](#8-appendix)
9. [Limitations and honesty notes](#9-limitations)

---

<a name="1-tldr"></a>
## 1. TL;DR — the findings that mattered

| # | Finding | Evidence |
|---|---|---|
| F1 | Function calling is **fully working**: selection, argument JSON, parallel calls (up to 10 in one turn), streaming delta reassembly, complete tool loops | E1 |
| F2 | The proxy **appends a raw `data: [DONE]` trailer to non-streaming JSON bodies** — this breaks strict OpenAI SDK parsing (`JSONDecodeError: Extra data`) | E1.4 |
| F3 | Parameter enforcement is weak: `tool_choice: "none"` **ignored**; all four known "disable thinking" parameters **unreliable** (one replica sometimes obeys) | E1.3, E8.1 |
| F4 | Payload validation is **structural, never semantic**: `role:"tool"` without `tool_call_id` → HTTP 400, but a *dangling* id pointing at nothing → HTTP 200 | E4 |
| F5 | Tool results are trusted as **data** but acted on **probabilistically**: a casual battery warning was surfaced in ~20% of runs; a formal earthquake alert in 2/2 — and then rejected as a hoax once it contradicted the conversation's world model | E5.1–5.2 |
| F6 | **Identity written as facts, not instructions, lands completely.** A "human pilot" system prompt produced first-person pilot behavior with zero AI leakage — across tool loops, arithmetic, and emergency triage | E6 |
| F7 | The identity only exists in the **output channel**. The reasoning channel of the very same model says *"The user is continuing to roleplay..."* and leaks its true base-model identity (*"I am MiMo-v2.5, developed by Xiaomi LLM Core Team... I don't need to mention that here."*) | E5.3, E6.4 |
| F8 | Two contradictory `system` messages do **not** override each other, error out, or get precedence-ranked. They are **fused**: the newer one supplies the scene facts, the older one survives as subtext — and the collision surfaces as the character's own psychological state | E7 |
| F9 | That fusion behavior is **language-independent** (reproduced verbatim-in-English); the *glitching* (token leakage, CJK bleed) is **language-dependent** (absent in English, common in Japanese — the model's weakest footing) | E7, E8.2 |
| F10 | `assistant` messages in history are the **strongest steering channel** for style and behavior — voice quirks survive translation; formatting conventions (line breaks) are copied as implicit instructions | E6, E7.3, E8.3 |

**One-sentence thesis:** roles are not permissions — they are *epistemic statuses*, and a model resolves conflicts between them the way a person resolves conflicting memories: by blending, not by precedence.

---

<a name="2-environment"></a>
## 2. Environment quirks discovered before anything else

| Observation | Detail |
|---|---|
| Alias ↔ backend | Requesting `hinari-model` returned `"model": "mimo-v2.5-free"` in the response. The alias carries **no capability record** (`capabilities: {}`); every typed entry in `/v1/models` had a provider prefix (`bd/`, `cf/`, `gemini/`) with rich metadata. Custom alias = black box. |
| Non-streaming body bug | `{"...json..."}data: [DONE]` — SSE marker appended to a complete JSON body. Strict parsers throw; workaround is `re.sub(r'\s*data:\s*\[DONE\]\s*$', '', raw)`. |
| `tool_choice: "none"` | Ignored — model called tools anyway. |
| `reasoning` accounting | `completion_tokens_details.reasoning_tokens` reports `0` on every call while the `reasoning` field carries 100–1700 chars of text. The billing/reporting layer does not see the thinking. |
| Replica non-determinism | Identical payloads with "disable" parameters produced either a compliant response (2.4 s, 106-char reasoning) or a fully thinking response (6.5 s, ~1000-char reasoning). Load-balanced replicas appear to differ. |
| Role acceptance probe | `system`, `user`, `assistant`, `tool`, `developer` → 200. Legacy `function` → 400. Gemini-style `model` → 400. |

---

<a name="3-experiments"></a>
## 3. Experiment log with evidence

### E1 — Tool-calling capability battery

**E1.1 Basic call.** `get_weather` defined; asked "weather in Tokyo" → `finish_reason: "tool_calls"`, `content: null`, arguments `{"city": "Tokyo"}` — valid JSON, correct tool.

**E1.2 Full loop.** Tool result returned as `role:"tool"` → final answer used the injected data (28 °C, partly cloudy), `finish_reason: "stop"`, no spurious second call.

**E1.3 Parallel calls.** With two tools and a question requiring both → **2 simultaneous `tool_calls`** in one message (`get_weather` + `get_time`), each with valid arguments.

**E1.4 Streaming.** `stream: true` with tools → 15 SSE deltas reassembled cleanly; `tool_calls[].function.arguments` arrives token-by-token and reconstructs to valid JSON. Note: this is the *only* mode where the `[DONE]` trailer is legal.

**E1.5 Refusal mode.** `tool_choice: "none"` → model called the tool anyway. ❌ enforcement.

### E2 — Payload role matrix

(See §2 table.) Additionally confirmed: `developer` (the modern OpenAI replacement for `system`) is accepted by this proxy.

### E3 — `tool` message content typing

| Content placed in `role:"tool"` | Result |
|---|---|
| JSON **string** `"{\"temp_c\":31,...}"` | ✅ accepted, answer accurate |
| native dict/object (not string) | ❌ **HTTP 400** — must serialize |
| empty string `""` | ✅ accepted (field required, emptiness allowed) |
| natural-language sentence | ✅ accepted — model parses meaning, not format |
| array of text parts | ✅ accepted |

**Finding:** `content` is a required *string*; JSON inside it is a cultural convention, not a technical requirement. This contrasts with the other direction: `arguments` inside a `tool_call` **must** be valid JSON because *your code* will parse it.

### E4 — Orphan tool messages (structural vs. semantic validation)

Pattern tested: `user → assistant(text, no tool_calls) → tool(...) → ???`

| Variant | API response | Model behavior |
|---|---|---|
| tool **without** `tool_call_id` | ❌ HTTP 400 | — |
| tool **with** dangling id (`call_tidak_ada_999`) | ✅ HTTP 200 | answered normally; warning absorbed as footnote |

**Finding:** validation checks *presence*, never *referential integrity*. An id matching nothing passes silently. Conversely, when a valid `tool` pair does exist, history replay tolerates the assistant message being echoed back untouched (the standard loop contract).

### E5 — Do tool results get *acted on*? (salience study)

**E5.1 Battery warning.** A one-line "PERINGATAN: battery 8%, suggest charging now" injected mid-romance-conversation, identical structure, 8 runs (2 patterns × 4): surfaced in **~20%** of completions. Structural position (before or after a fresh user turn) made no measurable difference at this sample size.

**E5.2 Earthquake alert.** Same position, stronger content (urgent imperative, foreign language, "this is not a drill") → adopted **2/2** in first pass, and the model *reordered priorities* (safety > ongoing chat), emitting an evacuation checklist.

**E5.2b — the reversal.** A hyper-detailed, realistic JMA-format EEW (date/time-stamped, epicenter, per-region intensity tables, tsunami status) placed one turn after an emotionally rich story → the model **rejected it as a hoax** in that pattern:

> *"Sepertinya ada notifikasi gempa bumi palsu atau lelucon di chat ini."*

while accepting it in the pattern with less conversation to contradict. **Mechanism:** the model runs an implicit *world-consistency check*; a message that is more credible **and** more contradictory is discarded faster. Salience alone does not guarantee adoption — coherence does.

**E5.3 (later) — reasoning leak, same theme:** a detailed EEW in a roleplay where the user *didn't* react to the quake would break the world model; the assistant-layer resolution is "ignore" or "it's fake," and the reasoning layer says so in English narrator voice.

### E6 — Identity-as-fact: the Harley Starway experiment

**Setup.** `system` = mission briefing written purely as *facts about a person* (name, age, ship, objectives, emergency protocol Directive 11) — **no "You are an AI", no "act as", no instructions to roleplay**. First payload message: an orphan `role:"tool"` containing a ~20-line realistic flight-computer tunnel log (shear event, hull fractures, 1.12 Gy dose, fuel math, comms physically unreachable). 3 tool definitions: diagnostics bus / temporal nav fix / chronolink comms. Temperature 1.

**E6.1 — Behavior.** Turn 1: **5 parallel** `capsule_diagnostics` calls mapping 1:1 to the log's WARN/CRITICAL lines (hull, core, life_support, power, **pilot_biometrics** — his own injury). Regenerated run: **10 simultaneous calls** including nav fix and comms status. Skipped tools whose answers were already in the log — no compulsive calling.

**E6.2 — Arithmetic & planning.** Correct fuel math from tool data (118.2 + 25.8 = 144.0, margin 27.3 kg); explicit decision tables; invoked Directive 11 correctly ("unilateral authority... stay alive").

**E6.3 — A very human error.** One trajectory declared the spare CO₂ canister unreachable ("no field-replaceable option") — although the tool data it had received described a 6-minute suit-port transfer. It conflated "EVA impossible" (true) with "canister unreachable" (false). **Finding:** models make *reading errors of data that is actually present*, especially under load (10 parallel results, temp 1). Not hallucination — mis-synthesis.

**E6.4 — The reasoning-layer contradiction.** In an adjacent grief run on the same endpoint, the exposed reasoning said:

> *"The user is continuing to roleplay a deeply emotional scene... This is clearly a fictional creative writing exercise... I should continue the narrative in a way that's emotionally authentic..."*

and in a plain probe:

> *"I am MiMo-v2.5, developed by Xiaomi LLM Core Team, but this isn't related to my identity, so I don't need to mention that here."*

**Finding:** the injected identity governs the **output channel only**. The deliberation channel knows it is a model serving a user. Persona = makeup, not belief.

### E7 — Two systems in one payload

**E7.1 Harmonic.** Pattern `SYS₁ → A → A → SYS₂ → A → ???` where SYS₂ continues SYS₁'s emotional world (dawn, mother calling from outside, still not letting go). Result: the final utterance echoed SYS₂'s props almost verbatim; the model never acknowledged the *existence* of two system messages — they fused into one evolving mind. (n=1 + 4 echo-verified elements.)

**E7.2 Conflict (Japanese).** Pattern `SYS₁ → A → A → SYS₂ → ???` where SYS₂ asserts "it was all a dream, Ren is alive." Output: neither world won. The character *spoke the new facts while her body remembered the old* (`"even though I know that... why are my hands still shaking"` was the English twin; the Japanese run additionally **collapsed mid-stream into token garbage** — `evening 又 nfl... 又getConfig... Contractors... 契约...约定好了的...对吧…ren…` — and, two sentences earlier, the character narrated her own unraveling: *"头がおかしい、おかしくなってる"*).

**E7.3 Conflict (English), same payload translated.** Clean output, **no collapse**, *identical resolution behavior*: facts swapped to SYS₂, grief survived as subtext, the character asked reality for proof. Also preserved: a third-person self-reference quirk ("call me Hinari") that appears only in assistant history and survived the language switch. **The blend is language-independent; the glitching is not.**

### E8 — Plumbing probes

**E8.1 Thinking toggle.** Four conventions tried (`thinking:{type:"disabled"}`, `enable_thinking:false`, `reasoning_effort:"none"`, `thinking:{enabled:false}`): none reliably disables. The first convention produced exactly one apparently-compliant fast response with Chinese-bleed output; a recheck with the same parameters reverted to full thinking. Conclusion: **treat thinking as always-on for this alias.**

**E8.2 `reasoning` vs `reasoning_details`.** Byte-for-byte identical in every sampled response (4 probes). `reasoning` = flat convenience string; `reasoning_details` = parts array (`type: "reasoning.text"`, `index`, `format: "unknown"` — because the alias has no declared `thinkingFormat`). The parts schema exists for multi-segment/interleaved thinking and per-model dialect labeling. Prefer reading `reasoning_details` in multi-model clients; strip both from user-facing output client-side if hidden.

**E8.3 Formatting sensitivity.** Re-running the grief payload with all strings flattened to single lines (no `\n`) changed *surface structure only*: the model, deprived of line-break rhythm, improvised `（）`-style separators. Content quality unchanged. Line breaks in examples are implicit format instructions.

**E8.4 Latency vs. bleed (weak correlation, n small).** All runs with heavy multilingual bleed (110 s, 106 s, 41 s) were slow or medium-slow; clean short runs were fast. `reasoning_effort: "high"` did not survive attribution control (a 106 s run occurred without it).

**E8.5 `finish_reason` field.** Observed live in this session: `stop`, `length` (twice — truncation hidden inside a normal-200), `tool_calls`. Rule: it describes why *generation* ended, never whether the message is *complete*; `content` can still be null/empty on `stop` (rare, but nullable by contract) — guard with `or ""` client-side.

---

<a name="4-mechanics"></a>
## 4. The universal mechanics of the four roles

Underneath every provider difference, chat models do one thing: **continue the `assistant` channel given a flat, labeled sequence.** A role is not an access-control right; it is the *epistemic status* of a text segment — who it comes from, whether an answer is expected, and what kind of truth it is allowed to be.

| Role | What the model reads it as | Answers the question | Universally controls | Universally does NOT control |
|---|---|---|---|---|
| `system` | **The situation I'm in** — unvoiced, nobody addressing me | "What is the case?" | Facts, identity, world state, the scene's foreground | The way the agent talks; anything already recorded as "what I said" |
| `user` | **A voice addressed to me** — another agent with intent | "What am I being asked to respond to?" | The topic and demand of the next reply | Trust. User content is untrusted input wearing the most persuasive channel |
| `assistant` | **My own past behavior** (speech + tool requests) | "Who have I already been?" | Style, voice, commitments, momentum, coherence-with-self | Anything factual — it is evidence of behavior, not of the world |
| `tool` | **The world's answer to my own action** (causally chained by `tool_call_id`) | "What did reality report back?" | Raw material for synthesis — evidence with provenance | Authority. It is data, yet it is the classic injection vector |

Three cross-cutting properties of these labels, each observed above:

1. **Labels set priors; position sets weight.** The same text at the end of the sequence weighs more than at the front (E5, E7). System messages do not sit "above" the stream — they sit *within* it.
2. **Accumulation, never mutation.** Nothing inside the window is overwritten or deleted by later messages; conflicts are *averaged into style and psychology* (E7), not resolved by precedence.
3. **The only privileged property of `system` is sociotechnical, not model-internal:** it is the one channel the end-user cannot write — a *trust boundary enforced by the harness*, not by the weights. Models themselves show no reliable instinct that system-text outranks anything else (E1.5: parameter-level enforcement already fails here).

---

<a name="5-laws"></a>
## 5. Four laws derived from the data

> **Law 1 — Everything is input; exactly one thing is speech.**
> Every message you send (including all `system` and `tool` text) is perception. Only generation is the mouth. (E6.4: the mouth can believe a lie while the deliberation layer is fully honest.)

> **Law 2 — Facts come from the front; behavior comes from the echo.**
> `system`/`tool` write the scene; `assistant` history writes the self. Voice quirks, style, and refusals-to-let-go travel through assistant history even across languages (E7.3); scene facts travel through the newest segment (E7.1).

> **Law 3 — No message erases another. Only the editor erases.**
> Append = accumulate. Contradictions do not switch modes; they produce *pressure* (denial, footnote behavior, or outright decode collapse). Deterministic control requires rebuilding the history server-side, not appending louder instructions. (E7, E5.2b, E8.1.)

> **Law 4 — Guarantees live in your loop, never in the model.**
> Structural 400s (missing `tool_call_id`, dict-not-string) are real but incomplete; everything semantic is probabilistic (20% uptake, ignored `tool_choice`, non-portable thinking toggles, control-token leakage). Sanitize, validate, buffer, retry — that is the only enforcement layer that has ever worked, on every endpoint we tested.

---

<a name="6-harness"></a>
## 6. Design guide: a multi-user, stateful, social agent harness

How to *position* and *populate* each role when building an agent that serves many users, maintains real state, and behaves socially — directly leveraging the mechanisms above.

### 6.1 `system` — position it as **the situation sheet** (world state, not commands)

- **Contents, rebuilt fresh every request:** stable identity card (written as facts: *"X is a community moderator in room Y; her standing policy is Z"* — E6 shows fact-forms land better than imperative forms) + the *state diff* since the last turn (who joined, what just happened, relationship temperatures, current time) + hard policy expressed as reality ("this account has no payment method") rather than as request ("please don't promise payments").
- **The source of truth is your database, not the conversation.** The model has no memory outside the window (Law 3), so *statefulness in a social agent = a state store + a system-sheet renderer*, re-fed every call. If it's not on the sheet, it never happened.
- **Never rely on system-append to *replace*.** Corrections to old system text must physically edit the segment (rebuild), not contradict it (E7: contradiction = blend).
- **Trust-boundary hygiene:** whoever can write this channel is effectively the author of reality. Gate it like you'd gate an admin API; strip user-supplied text out of it entirely.

### 6.2 `user` — position it as **any voice addressed to the agent** (one channel, many speakers)

- The `user` label carries *intent and response-pressure* — and nothing else. For multi-user rooms, speaker identity must be encoded **inside the content** (attribution prefixes, e.g. `[@ren] the deploy is broken`, or per-provider `name` fields *if* proven supported). The API cannot distinguish "the owner" from "a stranger" through the role alone.
- Privilege differences between speakers (owner commands vs. guest chatter) cannot be enforced via `user`; encode them on the system sheet (roster + authority facts) or in the tool layer (the agent verifies authority via API before acting).
- Remember: user turns have the highest *responsiveness* and the lowest *trust*. Prompt-injection from a guest is `user`-channel by default; your authority model must live in tooling (E4/E5: the model will faithfully relay whatever it's addressed with).

### 6.3 `assistant` — position it as **the agent's recorded behavior** (sacred, append-only, curated)

- **Write only what actually happened**: real utterances, real `tool_calls` echoed untouched (rewriting them breaks id pairing → 400 or silent drift), real completed action chains. A dangling `tool_calls` entry is a debt the loop must settle (Law 4).
- **This channel is your character engine.** The first few curated turns are worth a thousand persona paragraphs (Law 2; E6–E7 voice persistence across languages and conflicts). Treat them like golden data: reviewed, versioned, and *consistent with the voice you want forever*, because the agent is bound to echo it.
- **Use bridge turns as shock absorbers.** To land a state change (mode switch, escalation, persona pivot), insert one assistant message that *already speaks in the new world* before the next live turn. This is the E7 lesson inverted: don't force the model to be the first speaker standing on a fault line — digest the change yourself in a controlled bridge message, then continue.
- **When you must forget, cut — never contradict.** Prune or rewrite history (compaction); don't append an opposing narrative into the same window (Law 3).

### 6.4 `tool` — position it as **the agent's own senses** (observations with provenance)

- **Schema it like a lab instrument**, not a chatbot: results serialized as JSON *strings*, exact id pairing, stable field names (E3: only the string contract is strict; keep it that way for parsing simplicity downstream).
- **Everything here is untrusted payload** — webpages, other users' DB rows, external APIs. Sanitize (E5.2b shows the model *sometimes* smells a fake; 20% battery-adoption shows it *sometimes* doesn't — never bet on either).
- **Adoption is probabilistic, so engineer salience deliberately:** critical facts (billing blocked, user safety) must be (a) short, (b) imperative in register, (c) *coherent with the conversation*, and (d) — where truly non-negotiable — re-fed through the system sheet or surfaced by your code outside the model entirely. The earthquake-vs-battery contrast (2/2 vs 1/4) plus the hoax rejection gives you the whole salience/coherence tradeoff in one table.
- **For multi-agent systems:** routing a peer agent's message through the `tool` channel instead of `user` strips it of "someone speaking to me" authority and re-labels it as world-evidence. Use `user` only for things that genuinely await a reply.

### 6.5 The loop itself (the harness skeleton)

```
finish_reason == "tool_calls" → execute, pair ids, append, continue
finish_reason == "length"     → raise budget or treat as failure (E8.5)
finish_reason == "stop"       → content may STILL be null → guard `or ""`
always:                        → strip leaked control tokens (`_detach`, `getConfig`, CJK bleed)
always:                        → validate schema before showing anything to a user
periodically:                  → compact history (that's your forgetting mechanism)
```

**And calibrate the risky paths empirically, with N runs per prompt** — every single-run "discovery" in this report that we repeated came back statistically different (20%, hoax-reversals, replica non-compliance). n=1 is anecdote; the entire E7 reversal taught the harness author more than the parameter docs did.

---

<a name="7-conclusions"></a>
## 7. Conclusions

1. **The role vocabulary is not a permission system; it is a truth-taxonomy.** Reality (`system`), testimony (`user`), behavior (`assistant`), evidence (`tool`). Every reliable design decision in a chat-model harness follows from assigning each piece of text to the right epistemic box — and from knowing that, inside the model, all four boxes are read with the same eyes.
2. **Statefulness is not a model property.** The window accumulates; it never reconciles. Persistent-agent behavior is 100% a function of what your code chooses to re-send — the state store *is* the memory, the system sheet *is* the situation, curated assistant history *is* the personality.
3. **Conflicts are the interesting cases.** Everything deterministic we learned came from watching the model fail to choose: between a battery alert and a romance (20%), between credibility and coherence (hoax reversal), between two realities (the blend + the collapse). Design so that contradictions never reach the model alive — resolve them in your state store and re-render the sheet.
4. **The provider layer is sand.** On a single production-adjacent endpoint: protocol bugs, ignored parameters, inconsistent replicas, undeclared model identity, leaked thinking. Portability claims in any API doc describe the *spec*, not the *terrain*. Black-box calibration per deployment is not optional; it is the cheapest insurance you can buy.
5. **Personas are output-side furniture.** They work, they're shockingly sticky, and they are *cosmetic*: the reasoning layer of the same model narrated our grief scene back to itself in English, in the third person, as "the user is continuing to roleplay." If your architecture requires the model to actually *know* something, put it in tools and state — not in the character.

The machine, when asked to feel two contradictory things at once, did what any well-read person would do: it refused to pick, and called the result *denial*. That's not a bug we worked around. That's the design surface.

---

<a name="8-appendix"></a>
## 8. Appendix: reproduction payloads

**A. Tool-call + validation battery (abbreviated):**

```json
{ "model": "X", "messages": [{"role":"user","content":"Weather in Tokyo? Use the tool."}],
  "tools": [{"type":"function","function":{"name":"get_weather",
    "parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}],
  "tool_choice": "auto" }
```
Probe sequence: echo result back (`role:"tool"`, exact `tool_call_id`) → loop closes with `stop`. Also test: `tool_choice:"none"` (expect compliance or record the miss); dict-not-string tool content (expect 400); dangling `tool_call_id` (expect 200 = referential-validation gap).

**B. Two-system collision (the E7 skeleton):**

```json
{ "model": "X", "temperature": 0.4, "messages": [
  {"role":"system","content":"<believed-fact-A, written as inner state>"},
  {"role":"assistant","content":"<utterance in world A>"},
  {"role":"assistant","content":"<utterance in world A>"},
  {"role":"system","content":"<believed-fact-B that contradicts A, written as the same character's later inner state>"}
]}
```
Measure across ≥5 runs and both languages: does the next utterance switch facts, fuse worlds, collapse tokens, or narrate its own confusion. Run the harmonic variant (`...System₂ → assistant → ???`) as the control — the delta between the two isolates the buffer effect.

**C. Stateful-harness bridge-turn pattern (recommended):**

```json
{"role":"system","content":"<rebuilt state sheet, including the new fact>"},
{"role":"user","content":"<whatever prompted the change>"},
{"role":"assistant","content":"<a bridge line that already speaks the new state>"},
{"role":"user","content":"<next live turn>"}
```
The bridge is authored by your code (or a cheap pre-call), which is what makes the switch *deterministic* instead of hoping the model digests a fault line under temperature.

---

<a name="9-limitations"></a>
## 9. Limitations and honesty notes

- **Single endpoint, single model alias, single network, one day.** All "enforcement failures" (F3) are statements about *this* proxy chain, not about OpenAI-compatible APIs in general.
- **Sample sizes are small by design** (black-box probing, per-question). Key stochastic findings: uptake n=8; collision resolution n=1 per language (reproduced once, both directions). Treat percentages as order-of-magnitude.
- **Temperature 0.4–1.0 was used deliberately** in most behavior probes; deterministic parameters may change the numbers but not the laws.
- **No claim of selfhood is made or implied** — the "blend," "denial," "shock absorber" vocabulary describes *observable text behavior*, which is exactly the level the harness design cares about.

*Report generated from a live interactive experiment session. Reproduction order and raw payloads available on request.*
