import pytest
from securepass.strength import check_strength

def test_short_password():
    res = check_strength("aB3!", min_length=12)
    assert not res.ok
    assert any("Too short" in f for f in res.feedback)

def test_strong_password():
    pw = "A!f9qZpLmNs#2tUv"
    res = check_strength(pw, min_length=12)
    assert res.ok or res.score >= 4
    assert "Too short" not in " ".join(res.feedback)

