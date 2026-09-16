"""File persistence: runtime state only. Prompts are never written by the bot.

Layout under state/:
  harness.json   stamina/mood/relationship/activity/clock
  history.jsonl  append-only assistant/tool pairs (lore is rebuilt, not stored)
  memories/      one .md file per memory entry (1KB cap)

All writes are atomic (tmp + os.replace).
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from .. import config


class StoreError(Exception):
    pass


class FileStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or config.state_dir()
        self.memories_dir = self.root / "memories"
        self.root.mkdir(parents=True, exist_ok=True)
        self.memories_dir.mkdir(parents=True, exist_ok=True)

    # -- memories (the memory tool backend) --
    def list_memories(self) -> list[str]:
        return sorted(p.stem for p in self.memories_dir.glob("*.md"))

    def read_memory(self, name: str) -> str:
        path = self._memory_path(name)
        if not path.is_file():
            raise StoreError("not found")
        text = path.read_text(encoding="utf-8")
        return text[: config.MEM_MAX]

    def write_memory(self, name: str, body: str, now_min: int) -> dict:
        if len(body.encode("utf-8")) > config.MEM_MAX:
            raise StoreError("memory >1KB rejected")
        stamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        self._atomic_write(self._memory_path(name), f"{stamp}\n{body}")
        stored = {p.stem for p in self.memories_dir.glob("*.md")}
        broken = [p for p in _links(body) if p not in stored and p != name]
        return {"written": name, "broken": broken}

    def memories_dict(self) -> dict:
        return {name: self.read_memory(name) for name in self.list_memories()}

    def latest_note_tail(self, max_lines: int = 5) -> str:
        """Tail of the most recently modified memory file (system sheet slot)."""
        files = sorted(self.memories_dir.glob("*.md"), key=lambda p: p.stat().st_mtime)
        if not files:
            return ""
        lines = files[-1].read_text(encoding="utf-8").splitlines()
        return "\n".join(lines[-max_lines:])

    # -- harness snapshot --
    def save_harness(self, snapshot: dict) -> None:
        self._atomic_write(self.root / "harness.json", json.dumps(snapshot, indent=2))

    def load_harness(self) -> dict:
        path = self.root / "harness.json"
        if not path.is_file():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    # -- internals --
    def _memory_path(self, name: str) -> Path:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name).strip("_") or "untitled"
        return self.memories_dir / f"{safe}.md"

    def _atomic_write(self, path: Path, text: str) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)


def _links(text: str) -> list[str]:
    out: list[str] = []
    i = 0
    while (j := text.find("[[", i)) != -1:
        k = text.find("]]", j)
        if k == -1:
            break
        out.append(text[j + 2 : k])
        i = k + 2
    return out
