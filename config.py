# config.py
import os

BOT_NAME = os.environ.get("BOT_NAME", "TicaretSECURE")
TELEGRAM_TOKEN = os.environ.get("8214173862:AAGvwgiv6LwsfonD1Ed29EPRNxyZcq5AC4A")  # zorunlu
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
GEMINI_API_KEY = os.environ.get("AIzaSyDwuipLlDj7fsWgTXOSF1lEE6lXhbotWMc", None)

DATA_FILE = os.environ.get("DATA_FILE", "data.json")
WARN_LIMIT_MUTE = int(os.environ.get("WARN_LIMIT_MUTE", 3))
WARN_LIMIT_BAN = int(os.environ.get("WARN_LIMIT_BAN", 5))
XP_PER_MESSAGE = int(os.environ.get("XP_PER_MESSAGE", 1))
LOG_MAX = int(os.environ.get("LOG_MAX", 1000))

# runtime
PTB_VERSION = "20"
