"""Pipeline pseudocode for locked abstraction (v1). Stdlib only, no network.

Template files (owner-editable): SYSTEM.md + {identity} from IDENTITY.md,
pinned LORE.md as the assistant message right after system (never slides).
No <reality> block.

Nodes (source of truth for pipeline.png):
TRIGGER -> RENDER_SYSTEM -> PINNED_LORE -> CALL_LLM -> NORMALIZE -> MISS_HANDLER?
  -> DISPATCH[read_chat|scroll_chat|search_chat|send_message|do_activity|memory]
  -> UPDATE_STATE -> SLIDE_WINDOW -> APPEND -> (SLEEP_PATH | TRIGGER)
"""
from dataclasses import dataclass, field

CTX_BUDGET = 100_000
SCREEN = 7  # read_chat / scroll_chat page
SEARCH_HITS = 5  # search_chat(query) matches
SEARCH_WINDOW = 11  # search_chat(query, pick) window, picked is #6
PROTECT_LAST = 20  # newest pairs never slid out
STAMINA_MAX = 500
MEM_MAX = 1024  # 1KB per memory file

# ponytail: fixed constants, config file only when user asks to tune live


@dataclass
class State:
    now_min: int  # minutes since arbitrary epoch; harness clock
    stamina: float = STAMINA_MAX
    mood: int = 5
    last_wake: int = 0
    activity_until: int = 0
    activity_label: str = "idle"
    unread: int = 0
    mentioned: bool = False
    group: list = field(default_factory=list)  # [{from,time,text}] oldest->newest
    history: list = field(default_factory=list)  # [{role,content,tool_calls?}] pairs
    memories: dict = field(default_factory=dict)  # name -> text
    rel: dict = field(default_factory=dict)  # name -> score (-500..500)
    misses: int = 0


def need_wake(s: State) -> str | None:
    """TRIGGER. Returns reason or None (stay asleep, send no request)."""
    if s.now_min >= 60:  # 01:00 forced sleep stands in for wall clock in pseudocode
        return "force-01:00"
    if s.stamina <= 0:
        return "force-stamina"
    if s.now_min >= s.activity_until:
        return "until-reached"
    if s.mentioned or s.unread >= 20:  # @hinari or burst
        return "interrupted"
    return None


def render_system(s: State, identity_text: str) -> dict:
    """RENDER_SYSTEM. Template SYSTEM.md + {identity} from IDENTITY.md.

    No <reality> block. No raw chat text, no memory list.
    """
    return {
        "role": "system",
        "template": "SYSTEM.md",
        "identity": identity_text,
        "mood_snippet": f"mood={s.mood}",
        "stamina": round(s.stamina, 1),
        "activity": f"{s.activity_label} until {s.activity_until}",
        "group_meta": f"unread={s.unread} mentioned={s.mentioned}",  # counts only
        "now": s.now_min,
    }


def pinned_lore(lore_text: str) -> dict:
    """PINNED_LORE. Assistant message right after system, never slides.

    Content comes verbatim from owner-editable LORE.md (no char limit).
    This is the only assistant content kept; generated contents -> null.
    """
    return {"role": "assistant", "content": lore_text, "pinned": True}


def normalize(assistant_msg: dict) -> dict:
    """NORMALIZE. Drop content, keep tool_calls only (E1.2 pattern)."""
    return {"role": "assistant", "content": None,
            "tool_calls": assistant_msg.get("tool_calls", [])}


def handle_miss(s: State) -> str:
    """MISS_HANDLER. Content without tool_call = miss. Append nothing."""
    s.misses += 1
    if s.misses <= 1:
        return "retry-once"  # same system, one more CALL_LLM
    s.misses = 0
    s.activity_label, s.activity_until = "idle", s.now_min + 5  # SLEEP_PATH 5min
    return "sleep-5min"


def dispatch(s: State, call: dict):
    """DISPATCH. Returns (tool_result_dict, sleep_or_none)."""
    name, a = call["name"], call.get("args", {})
    if name == "read_chat":
        return {"chats": s.group[-SCREEN:]}, None
    if name == "scroll_chat":
        off = a.get("offset", 0)
        end = max(0, len(s.group) - off)
        return {"chats": s.group[max(0, end - SCREEN):end]}, None
    if name == "search_chat":
        q = a.get("query", "")
        hits = [m for m in s.group if q in m["text"]][:SEARCH_HITS]
        if "pick" in a:  # 11-window, picked is #6
            i = next(i for i, m in enumerate(s.group) if m is hits[a["pick"]])
            return {"chats": s.group[max(0, i - 5):i + 6]}, None
        return {"hits": hits}, None
    if name == "send_message":
        s.group.append({"from": "hinari", "time": s.now_min, "text": a["text"]})
        s.unread = 0
        return {"delivered": s.now_min}, None
    if name == "do_activity":
        s.activity_label, s.activity_until = a["label"], a["until"]
        return {"sleeping_until": a["until"]}, "sleep"
    if name == "memory":
        op = a["op"]
        if op == "list":
            return {"files": sorted(s.memories)}, None
        if op == "read":
            return {"text": s.memories[a["name"]]}, None
        body = a["text"]
        assert len(body.encode()) <= MEM_MAX, "memory >1KB rejected"
        s.memories[a["name"]] = body
        broken = [p for p in _links(body) if p not in s.memories and p != a["name"]]
        return {"written": a["name"], "broken": broken}, None
    raise ValueError(f"unknown tool {name}")


def _links(text: str) -> list:
    out, i = [], 0
    while (j := text.find("[[", i)) != -1:
        k = text.find("]]", j)
        if k == -1:
            break
        out.append(text[j + 2:k])
        i = k + 2
    return out


def slide_window(s: State) -> None:
    """SLIDE_WINDOW. history[0] is pinned LORE, never dropped.

    Pinned system is rebuilt (not stored); drop oldest whole pairs after lore.
    """
    while len(s.history) > PROTECT_LAST + 10 + 1:  # +1 lore; token est. stands in
        s.history.pop(1)


def demo():
    s = State(now_min=10, activity_until=50, unread=23, mentioned=True,
              group=[{"from": "ren", "time": i, "text": f"msg {i}"} for i in range(30)])
    assert need_wake(s) == "interrupted"  # mention wakes during sleep
    sys = render_system(s, "Hinari facts from IDENTITY.md")
    assert sys["template"] == "SYSTEM.md"
    assert "Hinari facts" in sys["identity"]
    assert "reality" not in str(sys), "no <reality> block"
    assert "msg " not in str(sys), "system must not carry raw chat text"
    assert "memories" not in str(sys).lower() or "files" not in str(sys)

    assert normalize({"content": "Saya AI siap membantu", "tool_calls": []}) == {
        "role": "assistant", "content": None, "tool_calls": []}
    assert handle_miss(s) == "retry-once" and handle_miss(s) == "sleep-5min"

    r, _ = dispatch(s, {"name": "read_chat"})
    assert len(r["chats"]) == 7 and r["chats"][-1]["text"] == "msg 29"
    r, _ = dispatch(s, {"name": "scroll_chat", "args": {"offset": 7}})
    assert len(r["chats"]) == 7 and r["chats"][-1]["text"] == "msg 22"
    r, _ = dispatch(s, {"name": "search_chat", "args": {"query": "msg 1"}})
    assert len(r["hits"]) <= 5
    r, _ = dispatch(s, {"name": "search_chat", "args": {"query": "msg 1", "pick": 2}})
    assert len(r["chats"]) == 11 and r["chats"][5]["text"] == "msg 11"  # picked is #6

    try:
        dispatch(s, {"name": "memory", "args": {"op": "write", "name": "a", "text": "x" * 2000}})
        raise AssertionError("must reject >1KB")
    except AssertionError as e:
        assert "1KB" in str(e)
    r, _ = dispatch(s, {"name": "memory",
                        "args": {"op": "write", "name": "m1", "text": "see [[ghost]]"}})
    assert r["broken"] == ["ghost"]

    s.stamina = 0
    assert need_wake(s) == "force-stamina"
    lore = pinned_lore("Aku Hinari, sejak SD aku memang orang yang..." + "x" * 5000)
    assert lore["content"].startswith("Aku Hinari")  # LORE.md verbatim, no char limit
    s.history = [lore] + list(range(40))
    slide_window(s)
    assert s.history[0] is lore, "pinned LORE never slides"
    assert len(s.history) == PROTECT_LAST + 10 + 1
    print("pipeline pseudocode OK")


if __name__ == "__main__":
    demo()
