"""Clean up Simplified Chinese that a model lets slip into a reply."""

from __future__ import annotations

from functools import lru_cache
from typing import Final

from opencc import OpenCC  # type: ignore[import-untyped]

# Big5 also contains these Simplified forms (后 is a valid character on its own,
# as in 皇后), so they survive the per-character pass and are fixed as whole words.
_WORD_FIXES: Final = {
    "關于": "關於",
    "之后": "之後",
    "以后": "以後",
    "然后": "然後",
    "最后": "最後",
    "結束后": "結束後",
}


@lru_cache
def _converter() -> OpenCC:
    return OpenCC("s2t")


def to_traditional(text: str) -> str:
    """Convert only characters Big5 cannot encode, which are Simplified-only forms.

    Running OpenCC over the whole reply rewrites correct Traditional text
    (台灣 becomes 臺灣, 了解 becomes 瞭解, 干擾 becomes 幹擾), so Big5 characters
    are left alone. This fixes characters, not mainland word choices.
    """

    def convert(char: str) -> str:
        try:
            char.encode("big5")
        except UnicodeEncodeError:
            return str(_converter().convert(char))
        return char

    converted = "".join(convert(char) for char in text)
    for wrong, right in _WORD_FIXES.items():
        converted = converted.replace(wrong, right)
    return converted
