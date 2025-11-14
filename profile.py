# profile.py
from telegram import Update
from telegram.ext import ContextTypes
from data_manager import DATA, save_data
from utils import uname_of, save_and_log
from config import XP_PER_MESSAGE

async def profil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uname = user.username or str(user.id)
    lvl = DATA.get("levels", {}).get(uname, 0)
    warns = DATA.get("warns", {}).get(uname, 0)
    puan = DATA.get("puanlar", {}).get(uname, 0)
    await update.message.reply_text(f"👤 @{user.username or user.first_name}\nSeviye: {lvl}\nUyarı: {warns}\nPuan: {puan}")

async def puan_goster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        uname = context.args[0].lstrip("@")
    else:
        uname = update.effective_user.username or str(update.effective_user.id)
    puan = DATA.get("puanlar", {}).get(uname, 0)
    await update.message.reply_text(f"🏆 @{uname} puanı: {puan}")

async def puan_ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # admin only in moderation normally — simplified here
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /puan_ver @kullanici miktar")
        return
    uname = context.args[0].lstrip("@")
    try:
        miktar = int(context.args[1])
    except:
        await update.message.reply_text("Miktar sayı olmalı.")
        return
    DATA.setdefault("puanlar", {})[uname] = DATA.setdefault("puanlar", {}).get(uname, 0) + miktar
    save_and_log("puan_ver", f"{uname}:{miktar}")
    save_data(DATA)
    await update.message.reply_text(f"✅ @{uname} puanı {miktar} eklendi. Toplam: {DATA['puanlar'][uname]}")
