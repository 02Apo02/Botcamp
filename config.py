# config.py
import os

BOT_NAME = os.environ.get("BOT_NAME", "TicaretSECURE")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # zorunlu
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)

DATA_FILE = os.environ.get("DATA_FILE", "data.json")
WARN_LIMIT_MUTE = int(os.environ.get("WARN_LIMIT_MUTE", 3))
WARN_LIMIT_BAN = int(os.environ.get("WARN_LIMIT_BAN", 5))
XP_PER_MESSAGE = int(os.environ.get("XP_PER_MESSAGE", 1))
LOG_MAX = int(os.environ.get("LOG_MAX", 1000))

# runtime
PTB_VERSION = "20"
