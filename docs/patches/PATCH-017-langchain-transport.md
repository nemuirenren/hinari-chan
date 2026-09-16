# PATCH-017 — LangChain transport (single adapter swap)

> Date: 2026-09-17. Artifacts `docs/archived_artefact/` are frozen and untouched.
> Owner intent; no YAGNI applied to the what, only to the how.

## What changed and why

The stdlib-urllib transport is retired. All LLM traffic now goes through
LangChain (`ChatOpenAI` against the configured OpenAI-compatible base URL),
so the model/provider pool widens without touching bot logic. One adapter,
total replacement — no dual-transport complexity.

Pre-tested before building: `ChatOpenRouter` was tried first and rejected —
its SDK hard-requires `system_fingerprint` in responses, which this proxy
never returns (model-independent failure). `ChatOpenAI`+`base_url` passed
every Hinari pattern live (basic call, closed loop, full 6-tool stack with
30k-char lore, heart stack, dangling-id tolerance, required choice).

## Design

- `hinari/adapters/llm.py` rewritten with an unchanged public surface
  (`TOOLS`, `LLMError`, `call_llm` signature): Hinari, heart, and compat
  call it exactly as before. urllib helpers (`post`, `parse_message`,
  `build_payload`, trailer strip) are deleted.
- Role mapping: system→`SystemMessage`, lore→`AIMessage`, history
  assistant→`AIMessage` (raw + normalized call forms), tool→`ToolMessage`,
  user→`HumanMessage`. Tool specs pass verbatim to `bind_tools`.
- Owner locks preserved: temperature only 1 / 0.4 (asserted), nothing else
  configured (`max_retries=0`, streaming off), `auto↔required` fallback kept,
  finish_reason from metadata with shape-inference fallback.
- Timeout trap recorded: LangChain timeouts are **milliseconds** — seconds
  are converted once in `_ms` (passing 240 raw would mean 0.24s).
- Deps: `langchain` 1.4.1 + `langchain-openai` 1.6.2 via `uv add` (today's
  lock). `langchain-openrouter` deliberately excluded (proven dead here).
- Compat probes run through the same adapter (dangling probe = unbound
  invoke, tools=None).

## Files

- Rewrote: `hinari/adapters/llm.py`, `hinari/compat.py` (probes via adapter),
  `tests/test_adapters.py`, `tests/test_startup.py`, `tests/test_heart.py`
  (tuple fakes), `README.md` (transport + deps lines).
- Edited: `pyproject.toml` / `uv.lock`.
- This doc.

## Verification

- 103 unit tests green (mapping, ms-timeout, no-extra-params, fallback).
- Live compat 4/4 + live boot (login, wake) on the real endpoint.
