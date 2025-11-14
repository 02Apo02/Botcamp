# vip.py
from telegram import Update
from telegram.ext import ContextTypes
from data_manager import DATA, save_data
from utils import save_and_log, is_admin

async def vip_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Bu komutu sadece adminler kullanabilir.")
        return
    if not context.args:
        await update.message.reply_text("Kullanım: /vip_ekle @kullanici")
        return
    uname = context.args[0].lstrip("@")
    if uname in DATA.get("vip", []):
        await update.message.reply_text(f"@{uname} zaten VIP.")
        return
    DATA.setdefault("vip", []).append(uname)
    save_and_log("vip_ekle", uname)
    save_data(DATA)
    await update.message.reply_text(f"✅ @{uname} VIP yapıldı.")

async def vip_cikar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Bu komutu sadece adminler kullanabilir.")
        return
    if not context.args:
        await update.message.reply_text("Kullanım: /vip_cikar @kullanici")
        return
    uname = context.args[0].lstrip("@")
    if uname in DATA.get("vip", []):
        DATA["vip"].remove(uname)
        save_and_log("vip_cikar", uname)
        save_data(DATA)
        await update.message.reply_text(f"✅ @{uname} VIP'den çıkarıldı.")
    else:
        await update.message.reply_text(f"@{uname} VIP değil.")

async def vip_liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vip = DATA.get("vip", [])
    if not vip:
        await update.message.reply_text("VIP yok.")
    else:
        await update.message.reply_text("VIP listesi:\n" + "\n".join([f"@{u}" for u in vip]))
