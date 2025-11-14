# moderation.py
import datetime
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from data_manager import DATA, save_data
from utils import save_and_log, uname_of, is_admin
from config import WARN_LIMIT_MUTE, WARN_LIMIT_BAN


async def warn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Bu komutu yalnızca adminler kullanabilir.")
        return
    # target
    target_user = None
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    elif context.args:
        arg = context.args[0].lstrip("@")
        target_user = {"username": arg}
    if not target_user:
        await update.message.reply_text("Kullanıcı belirtin (reply veya @kullanici).")
        return
    uname = target_user["username"] if isinstance(target_user, dict) else (target_user.username or str(target_user.id))
    DATA.setdefault("warns", {})[uname] = DATA.setdefault("warns", {}).get(uname, 0) + 1
    save_and_log("warn", f"{uname}:{DATA['warns'][uname]}")
    save_data(DATA)
    await update.message.reply_text(f"⚠️ @{uname} uyarıldı. Toplam: {DATA['warns'][uname]}")

    # otomatik cezalar
    if DATA['warns'][uname] >= WARN_LIMIT_BAN:
        try:
            if not isinstance(target_user, dict):
                await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
                save_and_log("auto_ban", uname)
                await update.message.reply_text(f"❌ @{uname} otomatik banlandı.")
            else:
                await update.message.reply_text("ID yok — manuel ban gerekebilir.")
        except Exception:
            await update.message.reply_text("Ban işlemi başarısız oldu.")
    elif DATA['warns'][uname] >= WARN_LIMIT_MUTE:
        try:
            if not isinstance(target_user, dict):
                until = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                permissions = ChatPermissions(can_send_messages=False)
                await context.bot.restrict_chat_member(update.effective_chat.id, target_user.id, permissions=permissions, until_date=until)
                save_and_log("auto_mute", uname)
                await update.message.reply_text(f"🔇 @{uname} 24 saat susturuldu.")
            else:
                await update.message.reply_text("ID yok — manuel mute gerekebilir.")
        except Exception:
            await update.message.reply_text("Mute işlemi başarısız oldu.")


async def uyari_sifirla_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Yalnızca adminler kullanabilir.")
        return
    target_user = None
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    elif context.args:
        target_user = {"username": context.args[0].lstrip("@")}    
    if not target_user:
        await update.message.reply_text("Kullanıcı belirtin.")
        return
    uname = target_user["username"] if isinstance(target_user, dict) else (target_user.username or str(target_user.id))
    DATA.setdefault("warns", {})[uname] = 0
    save_and_log("uyari_sifirla", uname)
    save_data(DATA)
    await update.message.reply_text(f"✅ @{uname} uyarıları sıfırlandı.")

async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Yalnızca adminler kullanabilir.")
        return
    target_user = None
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    else:
        await update.message.reply_text("Lütfen hedefin mesajına reply yapın.")
        return
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
        save_and_log("ban", target_user.username or str(target_user.id))
        await update.message.reply_text(f"🚫 @{target_user.username or target_user.id} banlandı.")
    except Exception:
        await update.message.reply_text("Ban başarısız. Bot admin olmalı.")

async def kick_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Yalnızca adminler kullanabilir.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply ile kullanıcıyı seçin.")
        return
    target_user = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
        await context.bot.unban_chat_member(update.effective_chat.id, target_user.id)
        save_and_log("kick", target_user.username or str(target_user.id))
        await update.message.reply_text(f"🦵 @{target_user.username or target_user.id} atıldı.")
    except Exception:
        await update.message.reply_text("Kick başarısız.")

async def mute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("Yalnızca adminler kullanabilir.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply ile kullanıcıyı seçin.")
        return
    target_user = update.message.reply_to_message.from_user
    try:
        until = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(update.effective_chat.id, target_user.id, permissions=permissions, until_date=until)
        save_and_log("mute", target_user.username or str(target_user.id))
        await update.message.reply_text(f"🔇 @{target_user.username or target_user.id} 24s susturuldu.")
    except Exception:
        await update.message.reply_text("Mute başarısız.")
