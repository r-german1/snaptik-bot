import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")

app = Client(
    "infinity_supreme_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    sleep_threshold=5
)

@app.on_message(filters.command("start"))
async def start_command_handler(client, message: Message):
    welcome_text = (
        "🌟 سڵاو ل تە هەڤاڵێ خۆشەویست!\n\n"
        "🤖 ئەڤە مەزنترین و پێشکەفتنترین بۆتا داونلۆدکرنێ یە ل جیهانێ، کو کوالیتیا 4K و MP3 بێ کێشە بۆ تە دئینە خوارێ.\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها یێ ئەڤێ بۆتێ: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دەستپێکرنێ، لینکێ ڤیدیۆیا خۆ (تیکتۆک، اینستاگرام، یوتیوب، سناپچات) ڕاستەوخۆ بۆ من بنێرە!"
    )
    
    welcome_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await message.reply_text(welcome_text, reply_markup=welcome_kb)

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def downloader_core_handler(client, message: Message):
    url_link = message.text.strip()
    if not url_link.startswith("http"):
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
        ])
        await message.reply_text(
            "⚠️ هیڤیە لینکەکا دروست و ڕاستەقینە بۆ من بنێرە برا!\n\n"
            "👑 خودان: @YUSEEF_SURCHI",
            reply_markup=err_kb
        )
        return

    process_msg = await message.reply_text(
        "⚡️ سیستەمێ ئینفینیتی: نوکە زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )

    try:
        ydl_opts = {'quiet': True, 'format': 'best'}
        with YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url_link, download=False)
            vid_title = video_info.get('title', 'Infinity Video')
            vid_time = video_info.get('duration', 0)
            
        action_kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📥 داونلۆدکرنا MP4 (4K)", callback_data=f"dl_mp4|{url_link}"),
                InlineKeyboardButton("🎵 داونلۆدکرنا MP3", callback_data=f"dl_mp3|{url_link}")
            ],
            [
                InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
            ]
        ])
        
        await process_msg.edit_text(
            f"🎬 ناڤێ ڤیدیۆیێ: {vid_title}\n"
            f"⏱ دەم: {vid_time} چرکه\n\n"
            "کوالیتیا خۆ هەڵبژێرە بۆ داونلۆدکرنێ 👇\n\n"
            "👑 خودان و بەرپرس: @YUSEEF_SURCHI",
            reply_markup=action_kb
        )
    except Exception as err:
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
        ])
        await process_msg.edit_text(
            f"❌ هەڵەیەک ڕوویدا د وەرگرتنا ڤیدیۆیێ دا:\n`{str(err)}`\n\n"
            "👑 خودان: @YUSEEF_SURCHI",
            reply_markup=err_kb
        )

print("🚀 Infinity Supreme Bot with Owner @YUSEEF_SURCHI is Running!")
app.run()
