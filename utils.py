# utils.py
import datetime
import logging
from typing import Any
from telegram import Update
from config import LOG_MAX
from data_manager import DATA, save_data

logger = logging.getLogger(__name__)


def save_and_log(action: str, info: Any):
    entry = {"time": datetime.datetime.utcnow().isoformat(), "action": action, "info": info}
    DATA.setdefault("logs", []).append(entry)
    if len(DATA["logs"]) > LOG_MAX:
        DATA["logs"] = DATA["logs"][-LOG_MAX:]
    save_data(DATA)


async def is_admin(update: Update) -> bool:
    try:
        member = await update.effective_chat.get_member(update.effective_user.id)
        return member.status in ["administrator", "creator"]
    except Exception:
        return False


def uname_of(user) -> str:
    if not user:
        return "unknown"
    return user.username or f"{user.first_name}_{user.id}"
