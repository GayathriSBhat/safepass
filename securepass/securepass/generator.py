from __future__ import annotations
import secrets
import string

DEFAULT_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/|~"

def generate_password(length: int = 20, require_symbol: bool = True, require_digit: bool = True,
                      require_upper: bool = True, require_lower: bool = True,
                      allow_symbols: bool = True) -> str:
    if length < 4:
        raise ValueError("length must be >= 4")
    pools = []
    if require_lower:
        pools.append(string.ascii_lowercase)
    if require_upper:
        pools.append(string.ascii_uppercase)
    if require_digit:
        pools.append(string.digits)
    if require_symbol and allow_symbols:
        pools.append(DEFAULT_SYMBOLS)

    # Start with guaranteed chars
    chosen = []
    for pool in pools:
        chosen.append(secrets.choice(pool))

    # Remaining pool is union of allowed characters
    allowed = string.ascii_lowercase + string.ascii_uppercase + string.digits
    if allow_symbols:
        allowed += DEFAULT_SYMBOLS

    while len(chosen) < length:
        chosen.append(secrets.choice(allowed))

    # Shuffle using secure shuffle
    for i in range(len(chosen)-1, 0, -1):
        j = secrets.randbelow(i+1)
        chosen[i], chosen[j] = chosen[j], chosen[i]

    return "".join(chosen)
