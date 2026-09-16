"""Runtime configuration: env loading, constants, 1-server/1-channel guard.

Stdlib only. This is the only place that reads process env / .env.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# ponytail: fixed constants, config file only when the owner asks to tune live.
SCREEN = 7  # read_chat / scroll_chat page size (LLD section 4)
SEARCH_HITS = 5  # search_chat(query) max hits
SEARCH_WINDOW = 11  # search_chat(query, pick) window, picked message is #6
CTX_BUDGET = 150_000  # warn-only telemetry threshold (Patch-015, not enforced)
HEART_BUDGET = 150_000  # warn-only telemetry threshold (Patch-015, not enforced)
MAX_PAIRS = 20  # sliding window size for Hinari and heart (Patch-015)
STAMINA_MAX = 500.0
MEM_MAX = 1024  # 1 KB per memory file, bytes
BURST_THRESHOLD = 6  # unread burst that interrupts sleep (Patch-014)
MAX_BUBBLES = 10  # max bubbles per send_message call (Patch-004)
CURFEW_START = 1  # curfew window start hour (inclusive, local time)
CURFEW_END = 5  # curfew window end hour (exclusive); 05:00+ is normal rules
MISS_SLEEP_MIN = 7  # idle sleep after exhausting misses (Patch-010)
MISS_MAX = 1  # consecutive misses before idle sleep (Patch-010)
MISS_PREVIEW = 300  # logged content preview chars per miss (Patch-016)
TOOL_LOOP_MAX = 12  # max tool iterations per wake
# ponytail: single wake ceiling against a runaway loop; raise only if observed.
TEMPERATURE = 1  # the only LLM sampling parameter ever sent for Hinari
HEART_TEMPERATURE = 0.4  # the only LLM sampling parameter ever sent for heart
HEART_TIMEOUT = 240  # seconds per heart call; fail-open past this
COMPAT_TIMEOUT = 240  # seconds per compat probe call
CALL_TIMEOUT = 240  # seconds per main-loop LLM call

REQUIRED_ENV = (
    "DISCORD_TOKEN",
    "DISCORD_GUILD_ID",
    "DISCORD_CHANNEL_ID",
    "LLM_BASE_URL",
    "LLM_API_KEY",
    "LLM_MODEL",
)


class ConfigError(Exception):
    """Raised when env/config is missing or malformed."""


def load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE lines from a .env file into os.environ (no override).

    Minimal stdlib reader so python-dotenv is not needed.
    """
    env_path = path or Path.cwd() / ".env"
    if not env_path.is_file():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class Config:
    discord_token: str
    guild_id: int
    channel_id: int
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    tool_choice: str = "auto"  # Patch-005: one value for Hinari, heart, compat

    @classmethod
    def from_env(cls) -> "Config":
        missing = [k for k in REQUIRED_ENV if not os.getenv(k)]
        if missing:
            raise ConfigError(
                "Missing required env vars: " + ", ".join(missing) + ". "
                "Copy .env.example to .env and fill it in."
            )
        try:
            guild_id = int(os.environ["DISCORD_GUILD_ID"])
            channel_id = int(os.environ["DISCORD_CHANNEL_ID"])
        except ValueError as exc:
            raise ConfigError("DISCORD_GUILD_ID/CHANNEL_ID must be integers.") from exc
        base_url = os.environ["LLM_BASE_URL"].rstrip("/")
        tool_choice = os.environ.get("TOOL_CHOICE", "auto").strip().lower()
        if tool_choice not in ("auto", "required"):
            raise ConfigError("TOOL_CHOICE must be auto or required.")
        return cls(
            discord_token=os.environ["DISCORD_TOKEN"],
            guild_id=guild_id,
            channel_id=channel_id,
            llm_base_url=base_url,
            llm_api_key=os.environ["LLM_API_KEY"],
            llm_model=os.environ["LLM_MODEL"],
            tool_choice=tool_choice,
        )


def is_allowed(guild_id: int, channel_id: int, cfg: Config) -> bool:
    """1-server/1-channel guard. Anything else is ignored, not an error."""
    return guild_id == cfg.guild_id and channel_id == cfg.channel_id


def prompts_dir() -> Path:
    return Path.cwd() / "prompts"


def state_dir() -> Path:
    return Path.cwd() / "state"


def log_file() -> Path:
    return Path.cwd() / "log.txt"
