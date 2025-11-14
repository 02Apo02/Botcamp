# data_manager.py
import json
import os
from typing import Dict, Any
from config import DATA_FILE

DEFAULT = {
    "kufur_listesi": ["örnek_kufur"],
    "reklam_listesi": ["t.me/", "http://", "https://"],
    "warns": {},
    "levels": {},
    "puanlar": {},
    "vip": [],
    "teminat_pos": {},
    "teminat_saha": {},
    "hatirlatmalar": {},
    "logs": [],
    "stats": {"messages": {}, "total_messages": 0}
}


def load_data() -> Dict[str, Any]:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    save_data(DEFAULT.copy())
    return DEFAULT.copy()


def save_data(d: Dict[str, Any]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


DATA = load_data()
