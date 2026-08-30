import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import yt_dlp

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU"
OWNER_ID = 8038533940
OWNER_NAME = "يوسف"

# کارکردن لەسەر چەندین سەرڤەر پێویستی بە تێپەڕاندنی سێشن هەیە
app = Client(
    "multi_server_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=64  # زیادکردنی ژمارەی کارمەندە ناوخۆییەکانی بۆتەکە بۆ توانای وەڵامدانەوەی خێرا لەسەر سەرڤەرە گەورەکان
)

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
        [InlineKeyboardButton("📢 کەناڵی ۱", url="https://t.me/mamzaga"), InlineKeyboardButton("📢 کەناڵی ۲", url="https://t.me/MAMxZAGROS")],
        [InlineKeyboardButton("📢 کەناڵی ۳", url="https://t.me/mamzagrosStore"), InlineKeyboardButton("📢 کەناڵی ۴", url="https://t.me/mamzagrosIPA")],
        [InlineKeyboardButton("📢 کەناڵی ۵", url="https://t.me/mamzagrosGroup"), InlineKeyboardButton("📢 کەناڵی ۶", url="https://t.me/mamzagrosinfo")],
        [InlineKeyboardButton("📢 کەناڵی ۷", url="https://t.me/mxbots1"), InlineKeyboardButton("📢 کەناڵی ۸", url="https://t.me/mamzagros")],
        [InlineKeyboardButton("✅ هەموویم جۆین کرد، پشکنین بکە", callback_data="check_join")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_media_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎬 داونلۆدی ڤیدیۆ (4K / MP4)", callback_data="dl_video"),
         InlineKeyboardButton("🎵 داونلۆدی دەنگ (MP3)", callback_data="dl_audio")]
    ]
    return InlineKeyboardMarkup(keyboard)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    is_joined = await check_subscription(client, user_id)
    
    if not is_joined:
        await message.reply_text(
            "سڵاو! بە خێر هاتیت بۆ بۆتی داونلۆدکەری پێشکەوتوو.\n"
            "بۆ بەکارهێنانی بۆتەکە، پێویستە سەرەتا لە هەموু کەناڵەکانی خوارەوە ئەندام (Join) ببیت! ⚠️\n\n"
            "دوای ئەوەی هەموویت جۆین کرد، دوگمەی پشکنین لە خوارەوە بگرە:",
            reply_markup=get_join_keyboard()
        )
        return

    await message.reply_text(
        f"سڵاو لە تو هه‌ڤاڵی خۆشەویست! ئەز بۆتێکی داونلۆدکرنی مە بە بەرزترین کوالیتی 4K و MP3 بێ وێنەڤەکرن (No Watermark).\n"
        f"خاوەنی ئەم بۆتە: **{OWNER_NAME}** 👑\n\n"
        "بۆ دەستپێکردن، لینکەی ڤیدیۆکەی (تیکتۆک، اینستاگرام، یوتیوب، سناپچات) بنێرە بۆم!"
    )

@app.on_callback_query(filters.regex("check_join"))
async def callback_check_join(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    is_joined = await check_subscription(client, user_id)
    
    if not is_joined:
        await callback_query.answer("تۆ هێشتا هەموو کەناڵەکانت جۆین نەکردووە! تکایە هەمویان جۆین بکە.", show_alert=True)
        return
    
    await callback_query.message.edit_text(
        f"پیرۆزە! تۆ هەموو کەناڵەکانت جۆین کرد ✅.\n"
        f"خاوەنی بۆت: **{OWNER_NAME}**.\n\n"
        "ئێستا لینکەکەی خۆت بنێرە تا کار بکەین!"
    )

user_links = {}

@app.on_message(filters.regex(r"https?://[^\s]+"))
async def receive_link(client, message):
    user_id = message.from_user.id
    is_joined = await check_subscription(client, user_id)
    
    if not is_joined:
        await message.reply_text(
            "ب بۆرینا تو! بۆ داونلۆدکرنا ڤیدیۆیان، پێویستە لەم کەناڵانەی خوارەوە ئەندام ببیت:",
            reply_markup=get_join_keyboard()
        )
        return

    url = message.text.strip()
    user_links[user_id] = url
    
    await message.reply_text(
        "فۆرماتی دابەزاندن هەڵبژێرە:",
        reply_markup=get_media_keyboard()
    )

@app.on_callback_query(filters.regex("^dl_"))
async def process_download(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    action = callback_query.data
    
    if user_id not in user_links:
        await callback_query.answer("ماوەی لینکەکە بەسەرچوو، تکایە جارێکی تر لینکەکەت بنێرە.", show_alert=True)
        return

    url = user_links[user_id]
    status_msg = await callback_query.message.edit_text("🔄 خەریکە زانیاری کۆدەکەینەوە و داونلۆد دەکەین...")

    os.makedirs("downloads", exist_ok=True)

    if action == "dl_video":
        ydl_opts = {
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]/best',
            'noplaylist': True,
        }
    else:
        ydl_opts = {
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'noplaylist': True,
        }

    try:
        def run_yt_dlp():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if action == "dl_audio":
                    base_f = ydl.prepare_filename(info)
                    return os.path.splitext(base_f)[0] + ".mp3", info.get('title', 'audio')
                else:
                    return ydl.prepare_filename(info), info.get('title', 'video')

        file_path, title = await asyncio.to_thread(run_yt_dlp)

        if action == "dl_video":
            await status_msg.edit_text("📤 خەریکە ڤیدیۆکە بە کوالیتاتی 4K بێ watermark دەنێردرێت...")
            await client.send_video(
                chat_id=user_id,
                video=file_path,
                caption=f"✨ ڤیدیۆکەت بە سەرکەوتوویی داونلۆد بوو!\n👤 خاوەنی بۆت: {OWNER_NAME}"
            )
        else:
            await status_msg.edit_text("📤 خەریکە دەنگەکە (MP3) دەنێردرێت...")
            await client.send_audio(
                chat_id=user_id,
                audio=file_path,
                title=title,
                performer=OWNER_NAME,
                caption=f"🎵 دەنگی ڤیدیۆکە داونلۆد بوو!\n👤 خاوەنی بۆت: {OWNER_NAME}"
            )

        if os.path.exists(file_path):
            os.remove(file_path)

        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ هەڵەیەک ڕوویدا لە کاتی داونلۆدکردن:\n`{str(e)}`")

if __name__ == "__main__":
    app.run()
