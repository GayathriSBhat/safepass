import re
from securepass.generator import generate_password, DEFAULT_SYMBOLS

def test_generate_default_length():
    pw = generate_password()
    assert 16 <= len(pw) <= 64 or len(pw) == 20
    assert any(c.islower() for c in pw)
    assert any(c.isupper() for c in pw)
    assert any(c.isdigit() for c in pw)
    assert any(c in DEFAULT_SYMBOLS for c in pw)

def test_generate_no_symbols():
    pw = generate_password(allow_symbols=False, require_symbol=False)
    assert all(c.isalnum() for c in pw)
