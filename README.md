# hinari-chan

![CI](https://github.com/nemuirenren/hinari-chan/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

A single human-like member living inside one Discord channel — not an
assistant bot. Hinari reads when she chooses, answers when she wants, and
stays silent the rest of the time. Selectivity, delay, and initiative come
from harness structure, never from prompting.

> Unofficial fan-inspired project. Not affiliated with any anime, studio, or
> rights holder.

---

## Table of contents

- [Features](#features)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Owner-editable surface](#owner-editable-surface)
- [Running 24/7](#running-247)
- [Tests](#tests)
- [Patches & artifacts](#patches--artifacts)
- [Project layout](#project-layout)
- [Contributing & branches](#contributing--branches)
- [License](#license)

---

## Features

- **One server, one channel.** Anything outside the configured guild/channel
  is ignored at the first line of the event handler.
- **Human shortcomings by construction.** Limited 7-bubble screen, truncated
  notifications (`unread` counts, mention/reply vibration), busyness, fatigue,
  night rest (01:00–04:59). Delay and silence are first-class outcomes.
- **No assistant-bot behavior.** No prefix commands, no slash commands. She
  talks only through `send_message` — including threaded `reply_to` quotes —
  or not at all.
- **Persistent inner life.** Stamina (0–500, exponential all-nighter collapse),
  gliding mood (0–10, eleven owner-written levels), per-person relationships
  (−500…+500, thirteen bands, factory-empty → Neutral).
- **Heart judge (background).** A second agent scores how words land on her
  (`warmth` −4…+2, `rel_delta` −30…+5 per call, +8/day upside cap, uncapped
  downside) through its own pinned-identity tool loop. Hinari never sees it.
- **Startup compatibility gate.** Every boot behaviorally probes the
  configured model (tool calling, loop closing, trailer tolerance, dangling-id
  tolerance). Incompatible model → exit 2 with a change-model message before
  Discord is ever touched. No model name is hardcoded anywhere.
- **No agent frameworks.** No LangChain/LangGraph. Dependencies: `discord.py`
  + `tiktoken`. LLM over stdlib `urllib`, state in plain files.
- **Token-measured windows + telemetry.** Both agents slide newest-20-pairs
  windows; every wake logs real token sizes with over-budget warnings.

---

## Quickstart

Prerequisites: Python ≥ 3.11, [uv](https://docs.astral.sh/uv/), a Discord
application with the **Message Content** privileged intent enabled, and any
OpenAI-compatible chat-completions endpoint with tool calling.

```bash
git clone https://github.com/nemuirenren/hinari-chan.git
cd hinari-chan
uv sync
cp .env.example .env   # then fill it in (table below)
uv run hinari
```

First boot runs the compatibility probes, logs in as Hinari, backfills the
latest 100 channel messages, and idles until something worth waking for.

---

## Configuration

`.env` (never committed):

| Key | Required | Default | Meaning |
|---|---|---|---|
| `DISCORD_TOKEN` | yes | — | Bot token (Message Content intent on in the portal) |
| `DISCORD_GUILD_ID` | yes | — | The one server id |
| `DISCORD_CHANNEL_ID` | yes | — | The one channel id |
| `LLM_BASE_URL` | yes | — | e.g. `http://localhost:20128/v1` |
| `LLM_API_KEY` | yes | — | Endpoint key (redacted from all logs) |
| `LLM_MODEL` | yes | — | Any compatible model; behaviorally gated, never defaulted |
| `TOOL_CHOICE` | no | `auto` | `auto` or `required`; drives Hinari, heart, and probes |

Locked constants live in `hinari/config.py` (only place besides `.env`):
`TEMPERATURE = 1` (Hinari), `HEART_TEMPERATURE = 0.4`, timeouts 240s,
`MAX_PAIRS = 20`, `CTX/HEART_BUDGET = 150k` (warn-only),
`MISS_MAX = 5` / `MISS_SLEEP_MIN = 5`, `BURST_THRESHOLD = 6`,
`MAX_BUBBLES = 10`, curfew `01:00–04:59`, page sizes `7/7/5/11`.

---

## Architecture

Single-process modular monolith — a pure core with thin adapters. Dependency
flows one way: `adapters → harness`. The harness never imports Discord,
network, env, or files.

```
Discord GW (1 guild, 1 ch)
  │ on_message → buffer + flags only (never calls the LLM)
  ▼
adapters/discord_phone ── 7/7/5→11 reads, bubble sends, reply refs
  ▼
harness/pipeline ── TRIGGER → RENDER → LORE → CALL_LLM → NORMALIZE
                     → MISS → DISPATCH → HEART → UPDATE → SLIDE → APPEND
  │                        ▲                  │
  │                   adapters/llm      adapters/store
  │                   (urllib, temp     (atomic JSON + 1KB
  │                    locked)           memories, [[link]] check)
  ▼
prompts/ ── SYSTEM / IDENTITY / LORE / HEART / moods / relationships
```

- Every guarantee lives in the loop (Law 4 of the role-mechanics research in
  `docs/research/`), never in the model.
- History appends real tool calls + real results only. Misses append nothing.
- Errors are never swallowed; each layer tags its module so tracebacks point
  at the area. Adapters fail open where a crash would corrupt state.

---

## Owner-editable surface

Everything characterizing *her* is a file, not code — edit and restart:

- `prompts/SYSTEM.md` — full-template system sheet (any new XML tags pass
  through verbatim; slot values stay counts/flags).
- `prompts/IDENTITY.md` — one source read by both Hinari and heart.
- `prompts/LORE.md` — pinned first-person history, no length limit.
- `prompts/HEART.md` — the background judge's rubric.
- `prompts/moods/` — 11 levels (`Ecstatic`…`Devastated`) + mapping.
- `prompts/relationships/` — 13 bands (`Devotion`…`Profound Hatred`) + mapping.
- `prompts/activities.json` — stamina multipliers + mood pleasantness.

---

## Running 24/7

| Script | Does |
|---|---|
| `./startup.sh` | Foreground run (`uv run hinari`) |
| `./startup.sh --install-service` | Installs system unit (sudo), enables + starts it |
| `./stop.sh` | `systemctl stop hinari` |
| `./reset.sh` | Stops service, wipes `state/` + `log.txt` (prompts/`.env` kept) |

Daily use: `systemctl status|start|stop|restart|disable hinari`,
`journalctl -u hinari -f` (plus the on-disk `./log.txt`, secrets redacted).
Factory state is full stamina, Flat mood, empty relationships.

---

## Tests

Stdlib `unittest` only — no network, Discord and the LLM always faked:

```bash
uv run python -m unittest discover -s tests
```

`tests/test_pipeline.py` is the locked v1 pseudocode spec (do not touch).
`test_harness / test_adapters / test_startup / test_heart / test_smoke`
cover triggers, pages, validation warnings, compat matrix, heart math,
payload locks, secret redaction, and the no-hardcoded-model ban (reads
`LLM_MODEL` from env, so set it to run that check).

---

## Patches & artifacts

- `docs/archived_artefact/` — frozen v1 design (LLD, Blueprint, pipeline visual).
- `docs/patches/PATCH-00X-*.md` — every change since, in order. Start here to
  understand why anything looks the way it does.
- `docs/research/` — the black-box role-mechanics experiments the design
  stands on. `docs/discord/` — local discord.py notes.

---

## Project layout

```
hinari-chan/
├─ pyproject.toml / uv.lock
├─ hinari/                 # runtime (config, compat, heart, tokens,
│  │                       # harness/{state,pipeline}, adapters/*, main)
├─ prompts/                # owner-editable character surface
├─ state/                  # runtime JSON (gitignored)
├─ tests/                  # stdlib suite + locked spec
├─ docs/{artifact,patches,research,discord}/
├─ startup.sh / stop.sh / reset.sh / log.txt (gitignored)
└─ .env.example / .env (gitignored)
```

---

## Contributing & branches

- `development` — daily integration. `main` — stable, protected (PR + green
  CI, no direct pushes).
- CI runs compile + full suite on both branches. Merging to `main` auto-
  deploys to the VPS (pull → sync → restart → health check).
- Every behavior change ships with a `docs/patches/PATCH-0XX-*.md` note.
  Artifacts are never edited.

---

## License

MIT — see [LICENSE](LICENSE).
