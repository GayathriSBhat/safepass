from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List

COMMON_PATTERNS = [
    r"(password|letmein|qwerty|12345|admin|welcome|iloveyou|monkey|dragon)",
]

@dataclass
class StrengthResult:
    ok: bool
    score: int
    feedback: List[str]

def check_strength(pw: str, min_length: int = 12, require_sets: bool = True) -> StrengthResult:
    feedback = []
    score = 0

    if len(pw) < min_length:
        feedback.append(f"Too short (min {min_length}).")
    else:
        score += 1

    sets = {
        "lower": any(c.islower() for c in pw),
        "upper": any(c.isupper() for c in pw),
        "digit": any(c.isdigit() for c in pw),
        "symbol": any(not c.isalnum() for c in pw),
    }
    missing = [k for k, v in sets.items() if not v]
    if require_sets and missing:
        feedback.append("Missing character classes: " + ", ".join(missing) + ".")
    else:
        score += 1

    # Repetition / sequences heuristic
    if re.search(r"(.)\1{2,}", pw):
        feedback.append("Contains repeated characters (e.g., 'aaa').")
    else:
        score += 1

    # Simple keyboard / dictionary-ish patterns
    for pat in COMMON_PATTERNS:
        if re.search(pat, pw, flags=re.IGNORECASE):
            feedback.append("Contains common word/pattern.")
            break
    else:
        score += 1

    # Entropy-ish heuristic: variety + length
    variety = sum([sets["lower"], sets["upper"], sets["digit"], sets["symbol"]])
    if variety >= 3 and len(pw) >= min_length + 4:
        score += 1
    elif variety < 2:
        feedback.append("Low variety of characters.")

    ok = (score >= 4) and not feedback
    return StrengthResult(ok=ok, score=score, feedback=feedback)
