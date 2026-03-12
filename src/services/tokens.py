"""Token counting utility using tiktoken."""

from __future__ import annotations

_encoder = None
_init_failed = False


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken cl100k_base. Falls back to len//4 on import error."""
    global _encoder, _init_failed
    if _encoder is None and not _init_failed:
        try:
            import tiktoken

            _encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:
            _init_failed = True
            return len(text) // 4
    if _encoder is None:
        return len(text) // 4
    try:
        return len(_encoder.encode(text))
    except Exception:
        return len(text) // 4
