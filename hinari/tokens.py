"""Token accounting via tiktoken (cl100k_base). Estimates, not gospel.

Exact only when the deployment's BPE matches; on third-party proxies it is a
close approximation — still orders better than entry counting.
"""

from __future__ import annotations

import json
import logging

log = logging.getLogger("hinari.tokens")

ENCODING = "cl100k_base"
PER_MESSAGE_OVERHEAD = 4  # chatML-ish priming; documented estimate

_enc = None


def _encoding():
    global _enc
    if _enc is None:
        import tiktoken

        _enc = tiktoken.get_encoding(ENCODING)
    return _enc


def count_message(msg: dict) -> int:
    text = json.dumps(msg, sort_keys=True, default=str)
    return len(_encoding().encode(text)) + PER_MESSAGE_OVERHEAD


def count(messages: list[dict]) -> int:
    return sum(count_message(m) for m in messages)
