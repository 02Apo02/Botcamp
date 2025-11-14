# ai_commands.py
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from config import GEMINI_API_KEY

async def ai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Kullanım: /ai <soru veya mesaj>")
        return

    prompt = " ".join(context.args)
    await update.message.reply_text("🤖 Düşünüyorum...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
                params={"key": GEMINI_API_KEY},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=60
            )
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                ai_text = data["candidates"][0]["content"]["parts"][0]["text"]
                await update.message.reply_text(ai_text[:4000])
            else:
                await update.message.reply_text("🤖 AI'den yanıt alınamadı.")

    except Exception as e:
        await update.message.reply_text(f"❌ AI komutunda hata: {e}")
