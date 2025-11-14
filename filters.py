# filters.py
from telegram import Update
from telegram.ext import ContextTypes
from data_manager import load_data, save_data
from moderation import warn_cmd
from utils import kurallar

data = load_data()

async def mesaj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user
    uname = user.username or str(user.id)

    # Mesaj sayacı
    data["stats"]["messages"][uname] = data["stats"]["messages"].get(uname, 0) + 1
    data["stats"]["total_messages"] += 1

    # Küfür kontrolü
    for kelime in data.get("küfür_listesi", []):
        if kelime in text:
            await update.message.reply_text(f"⚠️ @{uname}, lütfen küfür etme.")
            await warn_cmd(update, context)
            save_data(data)
            return

    # Reklam kontrolü
    for link in data.get("reklam_listesi", []):
        if link in text:
            await update.message.reply_text(f"🚫 @{uname}, reklam paylaşmak yasak!")
            await warn_cmd(update, context)
            save_data(data)
            return

    # POS veya saha mesajı
    if "pos" in text:
        if data.get("teminat_pos"):
            liste = ", ".join([f"@{u}" for u in data["teminat_pos"].keys()])
            await update.message.reply_text(f"💳 Teminatlı POS'cular: {liste}")
        else:
            await kurallar(update, context)
    elif "saha" in text:
        if data.get("teminat_saha"):
            liste = ", ".join([f"@{u}" for u in data["teminat_saha"].keys()])
            await update.message.reply_text(f"📍 Teminatlı Sahacılar: {liste}")
        else:
            await kurallar(update, context)

    save_data(data)
