"""Harness state: dataclass plus stamina/mood/relationship math.

Pure functions only (LLD section 6). The model never writes these directly.
Mirrors tests/test_pipeline.py pseudocode; that file stays the locked spec.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .. import config


@dataclass
class State:
    now_min: int  # harness clock, minutes since an arbitrary epoch
    stamina: float = config.STAMINA_MAX
    mood: int = 5
    last_wake: int = 0
    activity_until: int = 0
    activity_label: str = "idle"
    unread: int = 0
    mentioned: bool = False
    replied: bool = False  # someone replied to Hinari's own bubble (Patch-014)
    group: list = field(default_factory=list)  # [{from,time,text}] oldest->newest
    history: list = field(default_factory=list)  # assistant/tool pairs after lore
    rel: dict = field(default_factory=dict)  # name -> score (-500..500)
    misses: int = 0
    meta: dict = field(default_factory=dict)  # runtime bookkeeping (e.g. rel gain days)


def need_wake(s: State, curfew_fired: bool = False) -> str | None:
    """TRIGGER. Wake reason or None (stay asleep, send zero requests)."""
    if s.stamina <= 0:
        return "force-stamina"
    if curfew_fired:
        return "force-01:00"
    if s.now_min >= s.activity_until:
        return "until-reached"
    if s.mentioned or s.replied or s.unread >= config.BURST_THRESHOLD:
        return "interrupted"
    return None


def apply_stamina(
    s: State, awake_min: float, label: str, minutes: float, multiplier: float, asleep_min: float = 0.0
) -> float:
    """One harness stamina step, clamped to [0, max]."""
    hours_awake = awake_min / 60.0
    drain = 0.15 * math.exp(hours_awake / 6.0) * max(awake_min, 0.0)
    cost = max(minutes, 0.0) * multiplier * 0.5 if label != "idle" else 0.0
    recovery = max(asleep_min, 0.0) * 1.2
    s.stamina = min(config.STAMINA_MAX, max(0.0, s.stamina - drain - cost + recovery))
    return s.stamina


def next_mood(mood_old: int, stamina: float, activity_part: float, social_part: float) -> int:
    """Momentum update: moods glide, never teleport (LLD 6.2)."""
    stamina_part = 4 * (stamina / config.STAMINA_MAX) - 2
    target = 5 + stamina_part + activity_part + social_part
    target = min(10, max(0, target))
    return int(round(0.7 * mood_old + 0.3 * target))


def rel_gain(score: int) -> int:
    return min(500, score + 3)


def rel_loss(score: int) -> int:
    return max(-500, score - 5)


def rel_decay(score: int, idle_days: int) -> int:
    if idle_days <= 3 or score == 0:
        return score
    step = -1 if score > 0 else 1
    return score + step * int(0.2 * idle_days)
