# filters.py
from typing import Tuple
from data_manager import DATA


def check_kufur_reklam(text: str) -> Tuple[bool, str]:
    t = text.lower()
    for k in DATA.get("kufur_listesi", []):
        if k in t:
            return True, "kufur"
    for r in DATA.get("reklam_listesi", []):
        if r in t:
            return True, "reklam"
    return False, ""


def detect_pos_saha(text: str) -> Tuple[bool, bool]:
    t = text.lower()
    pos = "pos" in t
    saha = "saha" in t
    return pos, saha
