from __future__ import annotations
import hashlib
import requests
from typing import Tuple

HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{prefix}"

def sha1_hex(data: str) -> str:
    return hashlib.sha1(data.encode("utf-8")).hexdigest().upper()

def k_anonymity_query(password: str, timeout: float = 5.0) -> Tuple[bool, int]:
    """
    Returns (found, count) using HIBP k-anonymity (does NOT send full password).
    Raises requests.RequestException on network errors.
    """
    digest = sha1_hex(password)
    prefix, suffix = digest[:5], digest[5:]
    url = HIBP_RANGE_URL.format(prefix=prefix)
    headers = {"Add-Padding": "true", "User-Agent": "securepass/0.1"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    lines = resp.text.splitlines()
    for line in lines:
        parts = line.split(":")
        if len(parts) != 2:
            continue
        returned_suffix, count_str = parts
        if returned_suffix.strip().upper() == suffix:
            try:
                count = int(count_str.strip())
            except ValueError:
                count = 1
            return True, count
    return False, 0
