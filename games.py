# games.py
import random
from telegram import Update
from telegram.ext import ContextTypes
from data_manager import DATA, save_data
from utils import save_and_log

async def zar_at(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = random.randint(1,6)
    await update.message.reply_text(f"🎲 Zar: {r}")

async def sayi_tahmin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Kullanım: /sayi_tahmin <min> <max>")
        return
    try:
        a = int(context.args[0]); b = int(context.args[1])
    except:
        await update.message.reply_text("Geçerli sayılar girin.")
        return
    number = random.randint(a,b)
    context.user_data["sayi_tahmin"] = number
    await update.message.reply_text(f"Sayı tahmin oyunu başladı! {a}-{b} arasında tahmin için /tahmin <sayi>")

async def tahmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "sayi_tahmin" not in context.user_data:
        await update.message.reply_text("Önce /sayi_tahmin başlatın.")
        return
    if not context.args:
        await update.message.reply_text("Kullanım: /tahmin <sayi>")
        return
    try:
        guess = int(context.args[0])
    except:
        await update.message.reply_text("Geçerli sayı girin.")
        return
    number = context.user_data.get("sayi_tahmin")
    if guess == number:
        await update.message.reply_text("🎉 Doğru! Kazandınız.")
        del context.user_data["sayi_tahmin"]
    else:
        await update.message.reply_text(f"Yanlış. Doğru sayı {number} idi. /sayi_tahmin ile tekrar başlatabilirsiniz.")

async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reels = ["🍒","🍋","7️⃣","🔔","🍀"]
    res = [random.choice(reels) for _ in range(3)]
    await update.message.reply_text(" ".join(res))

# placeholder for many more game commands — we dynamically register many simple commands in main.py
