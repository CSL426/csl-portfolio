from __future__ import annotations

import json

from server.core.assistant_prompt import _PROFILE_PATH, build_assistant_instruction
from server.core.text import to_traditional


def test_simplified_characters_are_converted() -> None:
    assert to_traditional("不过我无法跨对话保留记忆") == "不過我無法跨對話保留記憶"


def test_simplified_words_that_big5_can_encode_are_fixed() -> None:
    assert to_traditional("对话结束后，关于这个，然后呢") == "對話結束後，關於這個，然後呢"


def test_correct_traditional_text_is_unchanged() -> None:
    # A whole-text OpenCC pass would rewrite 台灣, 了解 and 干擾. 啓 is outside
    # Big5, and it is in the owner's name.
    text = "廖啓舜 Spark，台灣，了解，干擾，皇后，裡面，後來 😀 C++ vLLM"
    assert to_traditional(text) == text


def test_english_is_unchanged() -> None:
    text = "Spark built a FastAPI service, then deployed it."
    assert to_traditional(text) == text


def test_instruction_contains_the_site_profile() -> None:
    instruction = build_assistant_instruction()
    profile = json.loads(_PROFILE_PATH.read_text(encoding="utf-8"))
    assert profile["resume"]["profile"]["nameZh"] in instruction
    assert all(project["name"] in instruction for project in profile["projects"])
    assert "繁體中文" in instruction
