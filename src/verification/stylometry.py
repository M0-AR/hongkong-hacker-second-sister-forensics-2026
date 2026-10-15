"""Style / stylometry check — verifies N's authorship claims (Ch.5-8).

N claims individuals leak identity via:
- paragraph leading spaces (Kwok-Tai: 3 spaces),
- sentence length / paragraphing (Siu-Man: short sentences),
- punctuation discipline (Violet: exact ellipsis; brother: commas, no periods),
- keyboard error patterns.
We implement a transparent, testable subset: leading-space histogram,
mean sentence length, comma/period ratio, ellipsis correctness.
"""
import re
from collections import Counter


def leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def paragraph_indent_profile(text: str) -> dict:
    lines = [l for l in text.splitlines() if l.strip()]
    counts = Counter(leading_spaces(l) for l in lines)
    return dict(sorted(counts.items()))


def sentence_stats(text: str) -> dict:
    sents = [s.strip() for s in re.split(r"[.!?。！？]+", text) if s.strip()]
    words = [len(s.split()) for s in sents] or [0]
    commas = text.count(",") + text.count("，")
    periods = text.count(".") + text.count("。")
    # ellipsis: correct Chinese ellipsis is exactly 6 dots ...... or ……
    ellipses = re.findall(r"\.{3,}|…+", text)
    correct = sum(1 for e in ellipses if e in ("......", "……"))
    return {
        "n_sentences": len(sents),
        "mean_words_per_sentence": round(sum(words)/len(words), 2),
        "commas": commas,
        "periods": periods,
        "comma_per_period": round(commas/max(1,periods), 2),
        "ellipsis_total": len(ellipses),
        "ellipsis_correct": correct,
    }


def kwok_tai_three_space_test(text: str) -> dict:
    prof = paragraph_indent_profile(text)
    total = sum(prof.values()) or 1
    three = prof.get(3, 0)
    return {"profile": prof, "p_three_space": round(three/total, 3)}
