"""Entry point: `uv run hinari`. Wiring only; guarantees live in the loop."""

from __future__ import annotations

import asyncio
import datetime
import logging
import math
import sys
import time
from pathlib import Path

from . import compat, config, heart, tokens
from .adapters import discord_phone, llm
from .adapters.discord_phone import Phone
from .adapters.store import FileStore
from .harness import pipeline, state
from .harness.state import State

log = logging.getLogger("hinari")


class _RedactFilter(logging.Filter):
    """Replace token/key substrings in log records (never log secrets)."""

    def __init__(self, secrets: list[str]) -> None:
        self._secrets = [s for s in secrets if s and len(s) > 6]

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for secret in self._secrets:
            if secret in msg:
                msg = msg.replace(secret, "***")
                record.msg, record.args = msg, ()
        return True


def setup_logging(log_path: Path, secrets: list[str]) -> None:
    handler_file = logging.FileHandler(log_path, encoding="utf-8")
    handler_out = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    handler_file.setFormatter(fmt)
    handler_out.setFormatter(fmt)
    filt = _RedactFilter(secrets)
    handler_file.addFilter(filt)
    handler_out.addFilter(filt)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler_file, handler_out]


def read_text_strict(path: Path, what: str) -> str:
    if not path.is_file():
        raise config.ConfigError(f"Missing required prompt file: {path} ({what})")
    return path.read_text(encoding="utf-8")


def load_prompts(base: Path) -> dict:
    """Load owner-editable surface. Minimal parsers so PyYAML is not needed."""
    identity = read_text_strict(base / "IDENTITY.md", "identity").strip()
    lore = read_text_strict(base / "LORE.md", "lore")
    system_tpl = read_text_strict(base / "SYSTEM.md", "system template")
    moods = _load_scored(base / "moods", "mood")
    bands = _load_scored(base / "relationships", "band")
    activities = _load_kv(base / "activities.json")
    return {
        "identity": identity,
        "lore": lore,
        "system_tpl": system_tpl,
        "heart": heart.load_heart_prompt(base),
        "moods": moods,
        "bands": bands,
        "activities": activities,
    }


def _load_kv(path: Path) -> dict:
    import json as _json

    if not path.is_file():
        return {}
    try:
        data = _json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except ValueError:
        return {}


def _load_scored(folder: Path, kind: str) -> dict:
    """Map score/index -> body text. Reads *.md (frontmatter-tolerant)."""
    out: dict = {}
    if not folder.is_dir():
        return out
    for path in sorted(folder.glob("*.md")):
        if path.name == "mapping.yaml":
            continue
        text = path.read_text(encoding="utf-8")
        body = text.split("---")[-1].strip() if text.startswith("---") else text.strip()
        score = _frontmatter_int(text, "score")
        out[path.stem if score is None else score] = body
    if not out:
        raise config.ConfigError(f"No {kind} files in {folder}")
    return out


def _frontmatter_int(text: str, key: str) -> int | None:
    if not text.startswith("---"):
        return None
    head = text.split("---", 2)[1]
    for line in head.splitlines():
        name, _, value = line.partition(":")
        if name.strip() == key:
            try:
                return int(value.strip())
            except ValueError:
                return None
    return None


def epoch_min() -> int:
    return int(time.time() // 60)


def curfew_active(now_hour: int | None = None) -> bool:
    hour = now_hour if now_hour is not None else datetime.datetime.now().hour
    return config.CURFEW_START <= hour < config.CURFEW_END


def minutes_to_full(stamina: float) -> int:
    return max(1, math.ceil((config.STAMINA_MAX - stamina) / 1.2))


def json_snapshot(rel: dict) -> str:
    import json as _json

    return _json.dumps({k: v for k, v in rel.items()}, default=str)[:500]


class Bot:
    def __init__(self, cfg: config.Config, prompts: dict, store: FileStore) -> None:
        self.cfg = cfg
        self.prompts = prompts
        self.store = store
        self.state = State(now_min=epoch_min())
        self.phone = Phone()
        self.memories: dict = {}
        self.heart_history: list = []
        self.heart_warmth: dict = {}
        self._restore()

    def _restore(self) -> None:
        snap = self.store.load_harness()
        for key in ("stamina", "mood", "last_wake", "activity_until", "activity_label",
                    "unread", "mentioned", "replied", "rel", "meta"):
            if key in snap:
                setattr(self.state, key, snap[key])
        self.state.group = snap.get("group", [])[-200:]
        self.state.history = snap.get("history", [])
        self.heart_history = snap.get("heart_history", [])
        self.state.now_min = epoch_min()
        self.memories = self.store.memories_dict()

    def _persist(self) -> None:
        self.store.save_harness(
            {
                "stamina": self.state.stamina,
                "mood": self.state.mood,
                "last_wake": self.state.last_wake,
                "activity_until": self.state.activity_until,
                "activity_label": self.state.activity_label,
                "unread": self.state.unread,
                "mentioned": self.state.mentioned,
                "replied": self.state.replied,
                "rel": self.state.rel,
                "meta": self.state.meta,
                "group": self.state.group[-200:],
                "history": self.state.history,
                "heart_history": self.heart_history,
            }
        )

    # -- wake cycle --
    async def tick(self, channel=None) -> None:
        self.state.now_min = epoch_min()
        reason = state.need_wake(
            self.state, curfew_fired=curfew_active() and self.state.stamina < config.STAMINA_MAX
        )
        if reason is None:
            return
        if reason in ("force-stamina", "force-01:00"):
            self._sleep_until_full(reason)
            self._persist()
            return
        await self._wake(reason, channel)
        self._persist()

    def _sleep_until_full(self, reason: str) -> None:
        mins = minutes_to_full(self.state.stamina)
        self.state.activity_label = "sleep"
        self.state.activity_until = self.state.now_min + mins
        self.state.last_wake = self.state.now_min
        state.apply_stamina(self.state, 0, "idle", 0, 0, asleep_min=mins)
        self.state.stamina = config.STAMINA_MAX
        log.info("sleep (%s) until +%dmin", reason, mins)

    async def _wake(self, reason: str, channel=None) -> None:
        s = self.state
        log.info("wake: %s unread=%d mentioned=%s replied=%s",
                 reason, s.unread, s.mentioned, s.replied)
        now_text = datetime.datetime.now().astimezone().strftime("%a, %Y-%m-%d, %H:%M %z")
        sys_msg = pipeline.render_system(
            s,
            self.prompts["system_tpl"],
            self.prompts["identity"],
            now_text,
            f"{s.activity_label} until {s.activity_until}",
            f"unread={s.unread} mentioned={s.mentioned} replied={s.replied}",
            memory_tail=self.store.latest_note_tail(),
            mood_text=str(self.prompts["moods"].get(s.mood, "")),
        )
        lore_msg = pipeline.pinned_lore(self.prompts["lore"])
        self.heart_warmth = {}
        for _ in range(config.TOOL_LOOP_MAX):
            messages = [sys_msg, lore_msg, *s.history]
            try:
                msg, _ = await asyncio.to_thread(
                    llm.call_llm,
                    self.cfg.llm_base_url, self.cfg.llm_api_key, self.cfg.llm_model, messages,
                )
            except llm.LLMError as exc:
                log.warning("CALL_LLM failed: %s", exc)
                msg = {"content": None, "tool_calls": []}
            msg = pipeline.normalize(msg)
            if not msg["tool_calls"]:
                if pipeline.handle_miss(s) == "retry-once":
                    continue
                log.info("miss x%d, idle sleep %dmin", config.MISS_MAX, config.MISS_SLEEP_MIN)
                break
            s.misses = 0
            for call in msg["tool_calls"]:
                result, sleep = await self._execute_call(call, channel)
                pipeline.append_pair(s, call, result)
                pipeline.slide_window(s)
                self._touch_state(call, result)
                if sleep == "sleep":
                    self._close_wake()
                    return
        self._close_wake()

    async def _execute_call(self, call: dict, channel=None) -> tuple[dict, str | None]:
        """Send goes to Discord first so history only keeps delivered lines."""
        name = call.get("name", "")
        args = call.get("args", {}) or {}
        if name == "send_message":
            items = pipeline._clean_bubbles(
                args, {m.get("message_id", 0) for m in self.state.group})
            if isinstance(items, dict):
                return items, None  # WARNING, Discord untouched, retry unlimited
            ids: list[int] = []
            if channel is not None:
                ids = await discord_phone.send_bubbles(channel, items)
                if not ids:
                    return {"error": "send failed"}, None
            result, _ = pipeline.dispatch(self.state, self.memories, call)
            if ids:
                self.state.group[-1]["message_id"] = ids[0]
                result = {**result, "message_ids": ids}
            if ids and len(ids) < len(items):
                result = {**result, "partial": True, "sent": len(ids)}
            return result, None
        result, sleep = pipeline.dispatch(self.state, self.memories, call)
        if name == "memory" and "written" in result:
            try:
                self.store.write_memory(result["written"], self.memories[result["written"]],
                                        self.state.now_min)
                self.memories[result["written"]] = self.store.read_memory(result["written"])
                result = {**result, "broken": [
                    p for p in pipeline._links(self.memories[result["written"]])
                    if p not in self.memories and p != result["written"]
                ]}
            except Exception as exc:  # store errors surface as tool results, not crashes
                log.warning("memory persist failed: %s", type(exc).__name__)
                return {"error": "persist failed"}, None
        await self._run_heart(name, call, result)
        return result, sleep

    async def _run_heart(self, name: str, call: dict, result: dict) -> None:
        """Judge read-path results in the background. Never alters tool results."""
        batch = self._heart_batch(name, call, result)
        if not batch:
            return
        args = call.get("args", {}) or {}
        snapshot = (
            f"mood={self.state.mood} rel={json_snapshot(self.state.rel)} "
            f"query={args.get('query', '')}"
        )
        try:
            assessments, additions = await asyncio.to_thread(
                heart.judge,
                self.cfg.llm_base_url, self.cfg.llm_api_key, self.cfg.llm_model,
                self.prompts["heart"], self.prompts["identity"],
                self.heart_history, batch, snapshot,
            )
        except Exception as exc:  # heart must never break the tool loop
            log.warning("heart failed: %s", type(exc).__name__)
            return
        self.heart_history.extend(additions)
        heart.slide_history(self.heart_history)
        day = self.state.now_min // 1440
        felt = heart.apply_assessments(self.state.rel, self.state.meta, day, assessments)
        self.heart_warmth.update(felt)
        if assessments:
            log.info("heart: %s", [(a["sender"], a["warmth"], a["rel_delta"]) for a in assessments])

    @staticmethod
    def _heart_batch(name: str, call: dict, result: dict) -> str:
        """Render read results as sender lines. Empty means nothing to judge."""
        if name in ("read_chat", "scroll_chat"):
            chats = result.get("chats", [])
        elif name == "search_chat":
            chats = result.get("chats", [])
            if not chats:
                return ""
        elif name == "memory" and (call.get("args", {}) or {}).get("op") == "read":
            text = result.get("text", "")
            return f"recalled note (own writing, not someone's words):\n{text}" if text else ""
        else:
            return ""
        lines = []
        for c in chats:
            line = f"{c.get('from', '?')}: {c.get('text', '')}"
            if c.get("reply_to") and c.get("quoted"):
                line += f" [replying to '{c['quoted'][:120]}']"
            lines.append(line)
        return "\n".join(lines)

    def _touch_state(self, call: dict, result: dict) -> None:
        s = self.state
        if call.get("name") == "do_activity" and "sleeping_until" in result:
            mins = max(0, result["sleeping_until"] - s.now_min)
            mult = float(self.prompts["activities"].get("multipliers", {}).get(
                call.get("args", {}).get("label", "idle"), 1.0))
            state.apply_stamina(s, mins, "active", mins, mult)

    def _close_wake(self) -> None:
        s = self.state
        ht, hh = tokens.count(s.history), tokens.count(self.heart_history)
        log.info("window: hinari=%dtok heart=%dtok", ht, hh)
        if ht > config.CTX_BUDGET:
            log.warning("hinari window over budget (%d)", ht)
        if hh > config.HEART_BUDGET:
            log.warning("heart window over budget (%d)", hh)
        pleasant = self.prompts["activities"].get("pleasantness", {})
        activity_part = float(pleasant.get(s.activity_label, 0.0))
        social = [(s.rel.get(n, 0) / 500) * 2 + w for n, w in self.heart_warmth.items()] or [0.0]
        s.mood = state.next_mood(s.mood, s.stamina, activity_part, sum(social) / len(social))
        day = s.now_min // 1440
        for name in list(s.rel):
            last_seen = s.meta.get(f"seen:{name}", day)
            if day - last_seen > 3:
                s.rel[name] = state.rel_decay(s.rel[name], day - last_seen)
        s.last_wake = s.now_min
        s.unread, s.mentioned, s.replied = 0, False, False


def main() -> None:
    config.load_dotenv()
    try:
        cfg = config.Config.from_env()
    except config.ConfigError as exc:
        print(f"hinari: bad config: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    setup_logging(config.log_file(), [cfg.discord_token, cfg.llm_api_key])
    log.info("hinari boot: guild=%s channel=%s", cfg.guild_id, cfg.channel_id)

    try:
        compat.check_compatible(cfg.llm_base_url, cfg.llm_api_key, cfg.llm_model,
                                cfg.tool_choice)
    except compat.CompatError as exc:
        log.error("incompatible model (probe=%s): %s. Change LLM_MODEL and retry.", exc.probe, exc.reason)
        print(f"hinari: model incompatible (probe={exc.probe}). Change LLM_MODEL and retry.",
              file=sys.stderr)
        raise SystemExit(2) from exc
    log.info("model compatibility check passed")

    try:
        prompts = load_prompts(config.prompts_dir())
    except config.ConfigError as exc:
        log.error("bad prompts: %s", exc)
        raise SystemExit(2) from exc

    store = FileStore()
    bot = Bot(cfg, prompts, store)

    import discord
    from discord.ext import tasks

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.guilds = True
    client = discord.Client(intents=intents)
    channel_ref: dict = {}

    @client.event
    async def on_ready() -> None:
        assert client.user is not None
        log.info("logged in as %s", client.user)
        ch = client.get_channel(cfg.channel_id)
        if ch is None:
            try:
                ch = await client.fetch_channel(cfg.channel_id)
            except Exception as exc:
                log.error("cannot access channel: %s", type(exc).__name__)
                await client.close()
                return
        if getattr(ch, "guild", None) is None or ch.guild.id != cfg.guild_id:
            log.error("channel is not in the configured guild; check IDs")
            await client.close()
            return
        channel_ref["channel"] = ch
        try:  # backfill latest history into the mirror buffer
            fetched = []
            async for m in ch.history(limit=100, oldest_first=False):
                ref = m.reference
                quoted = None
                if ref is not None and ref.resolved is not None:
                    quoted = getattr(ref.resolved, "content", None) or None
                fetched.append({
                    "id": m.id,
                    "from": m.author.display_name,
                    "from_id": m.author.id,
                    "time": int(m.created_at.timestamp() // 60),
                    "text": m.content or "",
                    "mention": client.user in m.mentions,
                    "reply_to": ref.message_id if ref is not None else None,
                    "quoted": quoted,
                })
            bot.phone.backfill(list(reversed(fetched)))
            bot.state.group = [
                {"message_id": m["id"], "from": m["from"], "time": m["time"],
                 "text": m["text"], "reply_to": m.get("reply_to"), "quoted": m.get("quoted")}
                for m in bot.phone.messages[-200:]
            ]
        except Exception as exc:
            log.warning("history backfill failed: %s", type(exc).__name__)
        checker.start()

    @client.event
    async def on_message(message) -> None:
        if client.user is None or message.author.id == client.user.id or message.author.bot:
            return
        if message.guild is None or not config.is_allowed(message.guild.id, message.channel.id, cfg):
            return
        name = message.author.display_name
        if name not in bot.state.rel:
            bot.state.rel[name] = 0  # factory-empty -> Neutral on first appearance
        bot.state.meta[f"seen:{name}"] = bot.state.now_min // 1440
        is_mention = client.user in message.mentions
        ref = message.reference
        reply_to = ref.message_id if ref is not None else None
        quoted = None
        if ref is not None:
            resolved = getattr(ref, "resolved", None)
            quoted = getattr(resolved, "content", None) or None
            if quoted is None and reply_to is not None:
                try:  # best effort; old messages may sit outside the cache
                    fetched = await message.channel.fetch_message(reply_to)
                    quoted = fetched.content or None
                except Exception:
                    quoted = None
        bot.phone.note_message(
            message.id, name, message.author.id,
            int(message.created_at.timestamp() // 60), message.content or "", is_mention,
            reply_to, quoted)
        bot.state.group.append({"message_id": message.id, "from": name,
                                "time": bot.state.now_min, "text": message.content or "",
                                "reply_to": reply_to, "quoted": quoted})
        bot.state.unread += 1
        if is_mention:
            bot.state.mentioned = True
        if pipeline.is_reply_to_own(bot.state.group, reply_to):
            bot.state.replied = True

    @tasks.loop(seconds=15)
    async def checker() -> None:
        try:
            await bot.tick(channel_ref.get("channel"))
        except Exception as exc:  # the loop must never die on a wake error
            log.warning("wake failed: %s: %s", type(exc).__name__, exc)

    @checker.before_loop
    async def _before() -> None:
        await client.wait_until_ready()

    client.run(cfg.discord_token)
