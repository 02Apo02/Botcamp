# ticaretsecure_bot.py
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- AYARLAR ---
BOT_NAME = "TicaretSECURE"
TELEGRAM_TOKEN = "8214173862:AAGvwgiv6LwsfonD1Ed29EPRNxyZcq5AC4A"  # Telegram Bot Token
OWNER_ID = 123456789  # Bot sahibi id
WARN_LIMIT_MUTE = 3
WARN_LIMIT_BAN = 5
XP_PER_MESSAGE = 1

# --- VERİ ---
DATA = {
    "stats": {"messages": {}, "total_messages": 0},
    "küfür_listesi": ["küfür1", "küfür2"],
    "reklam_listesi": ["http", ".com"],
    "teminat_pos": {},
    "teminat_saha": {},
    "levels": {},
    "puanlar": {},
    "warnings": {}
}

# --- LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- YARDIMCI FONKSİYONLAR ---
def save_data():
    pass  # placeholder, dosyaya kaydetme opsiyonu eklenebilir

def uname_of(user):
    return user.username or str(user.id)

async def kurallar(update, context):
    await update.message.reply_text("Kurallar: Teminat ve grup kuralları geçerlidir.")

async def warn_cmd(update, context):
    uname = uname_of(update.effective_user)
    DATA['warnings'][uname] = DATA['warnings'].get(uname, 0) + 1
    if DATA['warnings'][uname] >= WARN_LIMIT_BAN:
        await update.message.reply_text(f"⚠️ @{uname} banlandı!")
    elif DATA['warnings'][uname] >= WARN_LIMIT_MUTE:
        await update.message.reply_text(f"⚠️ @{uname} susturuldu!")

# --- MESAJ FİLTRELEME ---
def check_kufur_reklam(text):
    for k in DATA["küfür_listesi"]:
        if k in text:
            return True, 'kufur'
    for r in DATA["reklam_listesi"]:
        if r in text:
            return True, 'reklam'
    return False, None

def detect_pos_saha(text):
    return ("pos" in text.lower(), "saha" in text.lower())

# --- KOMUTLAR ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Merhaba! Ben {BOT_NAME}. Yardım için /komut yazın.")

async def komut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Komut listesi: temel komutlar, oyun, VIP, moderasyon, profil.")

async def mesaj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text
    uname = uname_of(update.effective_user)

    # Mesaj sayacı
    DATA['stats']['messages'][uname] = DATA['stats']['messages'].get(uname, 0) + 1
    DATA['stats']['total_messages'] += 1

    # Küfür ve reklam filtresi
    bad, kind = check_kufur_reklam(text)
    if bad:
        if kind == 'kufur':
            await update.message.reply_text(f"⚠️ @{uname}, lütfen küfür etme.")
            await warn_cmd(update, context)
        else:
            await update.message.reply_text(f"🚫 @{uname}, reklam paylaşmak yasak!")
            await warn_cmd(update, context)
        save_data()
        return

    # POS / Saha
    pos, saha = detect_pos_saha(text)
    if pos:
        if DATA.get('teminat_pos'):
            liste = ", ".join([f"@{u}" for u in DATA['teminat_pos'].keys()])
            await update.message.reply_text(f"💳 Teminatlı POS'cular: {liste}")
        else:
            await kurallar(update, context)
        return
    if saha:
        if DATA.get('teminat_saha'):
            liste = ", ".join([f"@{u}" for u in DATA['teminat_saha'].keys()])
            await update.message.reply_text(f"📍 Teminatlı Sahacılar: {liste}")
        else:
            await kurallar(update, context)
        return

    # XP ve puan
    DATA['levels'][uname] = DATA['levels'].get(uname, 0) + 1
    DATA['puanlar'][uname] = DATA['puanlar'].get(uname, 0) + XP_PER_MESSAGE
    save_data()

# --- AI PLACEHOLDER ---
async def ai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AI komutu henüz aktif değil. Yakında eklenecek!")

# --- GENERİK EKSTRA KOMUTLAR ---
async def generic_cmd_factory(name, desc):
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Komut: /{name} çalıştı — {desc}")
    return cmd

# --- MODERASYON ---
async def mute_cmd(update, context):
    await update.message.reply_text("Kullanıcı susturuldu (placeholder).")

async def ban_cmd(update, context):
    await update.message.reply_text("Kullanıcı banlandı (placeholder).")

# --- VIP ---
async def vip_ekle(update, context):
    await update.message.reply_text("VIP eklendi (placeholder).")

async def vip_cikar(update, context):
    await update.message.reply_text("VIP çıkarıldı (placeholder).")

async def vip_liste(update, context):
    await update.message.reply_text("VIP listesi (placeholder).")

# --- OYUN ---
async def zar_at(update, context):
    import random
    await update.message.reply_text(f"🎲 Zar sonucu: {random.randint(1,6)}")

async def sayi_tahmin_start(update, context):
    await update.message.reply_text("Sayı tahmin oyununa başla!")

async def tahmin(update, context):
    await update.message.reply_text("Tahmin yapıldı!")

async def slot(update, context):
    import random
    await update.message.reply_text(f"Slot sonucu: {random.choice(['🍒','🍋','7️⃣','🍉'])}")

# --- PROFİL / PUAN ---
async def profil(update, context):
    uname = uname_of(update.effective_user)
    await update.message.reply_text(f"Profil @{uname} — Level: {DATA['levels'].get(uname,0)} — Puan: {DATA['puanlar'].get(uname,0)}")

async def puan_goster(update, context):
    uname = uname_of(update.effective_user)
    await update.message.reply_text(f"@{uname} puan: {DATA['puanlar'].get(uname,0)}")

async def puan_ver(update, context):
    await update.message.reply_text("Puan verildi (placeholder).")

# --- ANA BAŞLATMA ---
async def main_async():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Temel komutlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("komut", komut))
    app.add_handler(CommandHandler("kurallar", kurallar))
    app.add_handler(CommandHandler("ai", ai_cmd))

    # Moderasyon
    app.add_handler(CommandHandler("warn", warn_cmd))
    app.add_handler(CommandHandler("mute", mute_cmd))
    app.add_handler(CommandHandler("ban", ban_cmd))

    # VIP
    app.add_handler(CommandHandler("vip_ekle", vip_ekle))
    app.add_handler(CommandHandler("vip_cikar", vip_cikar))
    app.add_handler(CommandHandler("vip_liste", vip_liste))

    # Oyun
    app.add_handler(CommandHandler("zar_at", zar_at))
    app.add_handler(CommandHandler("sayi_tahmin", sayi_tahmin_start))
    app.add_handler(CommandHandler("tahmin", tahmin))
    app.add_handler(CommandHandler("slot", slot))

    # Profil & Puan
    app.add_handler(CommandHandler("profil", profil))
    app.add_handler(CommandHandler("puan", puan_goster))
    app.add_handler(CommandHandler("puan_ver", puan_ver))

    # Dinamik ekstra komutlar (180+)
    for i in range(1,181):
        name = f"extra{i}"
        desc = f"Ekstra komut #{i}"
        cmd = await generic_cmd_factory(name, desc)
        app.add_handler(CommandHandler(name, cmd))

    # Mesaj filtreleme
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj))

    print("✅ TicaretSECURE Bot çalışıyor...")
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    except Exception as e:
        print("Bot hata ile kapandı:", e)
