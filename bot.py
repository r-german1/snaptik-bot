import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# زانیاریێن بۆتی و خودانی
API_ID = int(os.environ.get("API_ID", "0"))  # ل سەر Railway دڤێت ب دەی
API_HASH = os.environ.get("API_HASH", "")    # ل سەر Railway دڤێت ب دەی
BOT_TOKEN = "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU"
OWNER_ID = 8038533940
OWNER_NAME = "ZAGROS"

app = Client("downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ٨ کەناڵێن مەرج بۆ Join بوونێ
CHANNELS = [
    "mamzaga",
    "MAMxZAGROS",
    "mamzagrosStore",
    "mamzagrosIPA",
    "mamzagrosGroup",
    "mamzagrosinfo",
    "mxbots1",
    "mamzagros"
]

async def check_subscription(client, user_id):
    # ئەگەر ئەڤ کەسە خودانێ بۆتی بیت، پێدڤی نینە پشکنینا کەناڵان بۆ بکەین (بۆ هندێ تو بێ کێشە تێستی بکەی)
    if user_id == OWNER_ID:
        return True
        
    for channel in CHANNELS:
        try:
            member = await client.get_chat_member(f"@{channel}", user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception:
            pass
    return True

def get_join_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 کەناڵێ ١", url="https://t.me/mamzaga"), InlineKeyboardButton("📢 کەناڵێ ٢", url="https://t.me/MAMxZAGROS")],
        [InlineKeyboardButton("📢 کەناڵێ ٣", url="https://t.me/mamzagrosStore"), InlineKeyboardButton("📢 کەناڵێ ٤", url="https://t.me/mamzagrosIPA")],
        [InlineKeyboardButton("📢 کەناڵێ ٥", url="https://t.me/mamzagrosGroup"), InlineKeyboardButton("📢 کەناڵێ ٦", url="https://t.me/mamzagrosinfo")],
        [InlineKeyboardButton("📢 کەناڵێ ٧", url="https://t.me/mxbots1"), InlineKeyboardButton("📢 کەناڵێ ٨", url="https://t.me/mamzagros")],
        [InlineKeyboardButton("✅ من هەمی join کرین، پشکنین بکە", callback_data="check_join")]
    ]
    return InlineKeyboardMarkup(keyboard)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    is_joined = await check_subscription(client, user_id)
    
    if not is_joined:
        await message.reply_text(
            "سلاڤ! ب خێر هاتنی بۆ بۆتێ داونلۆدکرنێ.\n"
            "بۆ بکارئینانا بۆتی، پێدڤییە پاشکو ئەڤان کەناڵێن ل خوارێ هەمیان Join بکەی! ⚠️\n\n"
            "پشتی تە هەمی join کرین، دوگمەیا پشکنینێ ل خوارێ کلیک بکە:",
            reply_markup=get_join_keyboard()
        )
        return

    await message.reply_text(
        f"سلاڤ ل تە هه‌ڤالێ هێژا! ئەز بۆتەکێ داونلۆدکرنێ مە ب کوالیتیا بلندا 4K و MP3 بێ watermark بۆ هەمی کەسان.\n"
        f"خودانێ ڤی بۆتی: **{OWNER_NAME}** 👑\n\n"
        "نۆکە لینکێ ڤیدیۆیا خۆ بۆ من بنێرە دا بۆ تە داونلۆد بکەم!"
    )

@app.on_callback_query(filters.regex("check_join"))
async def callback_check_join(client, callback_query):
    user_id = callback_query.from_user.id
    is_joined = await check_subscription(client, user_id)
    
    if not is_joined:
        await callback_query.answer("تە هنەک کەناڵ هێشتا join نەکربوون! تکایە هەمیان join بکە.", show_alert=True)
        return
    
    await callback_query.message.edit_text(
        f"پیرۆزە! تە هەمی کەناڵ join کرین ✅.\n"
        f"خودانێ بۆتی: **{OWNER_NAME}**.\n\n"
        "نوکە لینکێ خۆ بنێرە دا کار بکەین!"
    )

@app.on_message(filters.regex(r"https?://[^\s]+"))
async def download_media(client, message):
    user_id = message.from_user.id
    is_joined = await check_subscription(client, user_id)
    
    if not is_joined:
        await message.reply_text(
            "ب بۆرینا تە! بۆ وێ چەندێ بتشێ ڤیدیۆیان داونلۆد بکەی، پێدڤییە پاشکو ل ڤان کەناڵان هەمیان join ببی:",
            reply_markup=get_join_keyboard()
        )
        return

    url = message.text.strip()
    status_msg = await message.reply_text("🔄 جارە زانیاری دهێنە کومکرن و ب کوالیتیا 4K وێڤەدەکرن...")

    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]/best',
        'noplaylist': True,
    }

    try:
        def run_yt_dlp():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info), info.get('title', 'video')

        file_path, title = await asyncio.to_thread(run_yt_dlp)

        await status_msg.edit_text("📤 نوکە ڤیدیۆ ب بێ watermark و کوالیتیا بلندا 4K دهێتە هنارتن...")
        await message.reply_video(video=file_path, caption=f"✨ ڤیدیۆیا تە هاتە داونلۆدکرن!\nخودانێ بۆتی: {OWNER_NAME}")

        if os.path.exists(file_path):
            os.remove(file_path)

        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ خەلەتیەک د داونلۆدکرنێ دا چێبوو:\n`{str(e)}`")

if __name__ == "__main__":
    app.run()
