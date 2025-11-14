# config.py
import os

# Bot adı
BOT_NAME = os.environ.get("BOT_NAME", "TicaretSECURE")

# Telegram bot token (zorunlu)
# Railway veya başka bir ortamda TELEGRAM_TOKEN ortam değişkeni tanımlı olmalı
TELEGRAM_TOKEN = os.environ.get(
    "TELEGRAM_TOKEN", 
    "8214173862:AAGvwgiv6LwsfonD1Ed29EPRNxyZcq5AC4A"  # Varsayılan token (local test için)
)

# Bot sahibi ID
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# Gemini AI API key (isteğe bağlı, şimdilik None)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)

# Veri dosyası
DATA_FILE = os.environ.get("DATA_FILE", "data.json")

# Uyarı limitleri
WARN_LIMIT_MUTE = int(os.environ.get("WARN_LIMIT_MUTE", 3))
WARN_LIMIT_BAN = int(os.environ.get("WARN_LIMIT_BAN", 5))

# XP sistemi
XP_PER_MESSAGE = int(os.environ.get("XP_PER_MESSAGE", 1))

# Log ayarları
LOG_MAX = int(os.environ.get("LOG_MAX", 1000))

# PyTelegramBotAPI / python-telegram-bot sürümü
PTB_VERSION = "20"
