import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")

CHANNELS = [
    "@mamzagrosProfile",
    "@mamzaga",
    "@MAMxZAGROS",
    "@mamzagrosStore",
    "@mamzagrosIPA",
    "@mamzagrosGroup",
    "@mamzagrosinfo",
    "@mamzagros",
    "@mxbots1"
]

app = Client(
    "infinity_supreme_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    sleep_threshold=5
)

async def check_all_channels(client, user_id):
    tasks = []
    for channel in CHANNELS:
        async def verify(ch):
            try:
                member = await client.get_chat_member(ch, user_id)
                return member.status in ["member", "administrator", "creator"]
            except Exception:
                return False
        tasks.append(verify(channel))
    
    results = await asyncio.gather(*tasks)
    return all(results)

@app.on_message(filters.command("start"))
async def start_command_handler(client, message: Message):
    user_id = message.from_user.id
    is_joined = await check_all_channels(client, user_id)
    
    if not is_joined:
        buttons = []
        for index, ch_name in enumerate(CHANNELS, 1):
            clean_ch = ch_name.replace('@', '')
            buttons.append([InlineKeyboardButton(f"📢 بەشداربە لە کەناڵی {index}", url=f"https://t.me/{clean_ch}")])
        
        buttons.append([InlineKeyboardButton("🔄 پشکنینی بەشداربوونی ئینفینیتی", callback_data="check_sub")])
        buttons.append([InlineKeyboardButton("👑 پەیوەندی بە خاوەن: @X_MAM6", url="https://t.me/X_MAM6")])
        keyboard = InlineKeyboardMarkup(buttons)
        
        await message.reply_text(
            "⚠️ ئاگاداری لە سیستەمی خاوەن @X_MAM6:\n\n"
            "بۆ ئەوەی بتوانیت لەم بۆتە بێسنوورە کەڵک وەربگریت، دەبێت سەرەتا لە هەموو ئەم کەناڵانەی خوارەوە بەشدار ببیت!\n\n"
            "پشتی بەشداربوون، دوگمەی پشکنین کلیک بکە 👇\n\n"
            "👑 خاوەن: @X_MAM6",
            reply_markup=keyboard
        )
        return

    welcome_text = (
        "🌟 سڵاو لە تو هەڤاڵی خۆشەویست!\n\n"
        "🤖 ئەمە مەزنترین و پێشکەوتووترین بۆتی داونلۆدکردنی جیهانە بێ هیچ سنوورەکێ کو کوالیتیا 4K و MP3 بێ کێشە پێشکەش دکەت.\n\n"
        "👑 خاوەن و دامەزرێنەری ڕەهای ئەم بۆتە: @X_MAM6\n\n"
        "🔗 بۆ دەستپێکردن، لینکەی ڤیدیۆکەی (تیکتۆک، اینستاگرام، یوتیوب، سناپچات) بنێرە بۆم بۆ داونلۆدکرنێ!"
    )
    
    welcome_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 خاوەن: @X_MAM6", url="https://t.me/X_MAM6")]
    ])
    await message.reply_text(welcome_text, reply_markup=welcome_kb)

@app.on_callback_query(filters.regex("check_sub"))
async def callback_check_subscription(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    is_joined = await check_all_channels(client, user_id)
    
    if not is_joined:
        await callback_query.answer("❌ هێشتا لە هەموو کەناڵەکان بەشدار نەکردوویت!\n👑 خاوەن: @X_MAM6", show_alert=True)
        return
    
    await callback_query.answer("✅ پیرۆزە! ئێستا دەتوانیت ڤیدیۆ بنێریت.\n👑 خاوەن: @X_MAM6", show_alert=True)
    
    success_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 خاوەن: @X_MAM6", url="https://t.me/X_MAM6")]
    ])
    
    await callback_query.message.edit_text(
        "🌟 **سوپاس بۆ بەشداربوونا تە ل هەمی کەناڵان!**\n\n"
        "🤖 ئێستا بۆتەکەی مە ئامادەیە. لینکەی ڤیدیۆیا خۆ (تیکتۆک، اینستاگرام، یوتیوب، سناپچات) بنێرە بۆم!\n\n"
        "👑 خاوەن و بەرپرس: @X_MAM6",
        reply_markup=success_kb
    )

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def downloader_core_handler(client, message: Message):
    user_id = message.from_user.id
    is_joined = await check_all_channels(client, user_id)
    
    if not is_joined:
        buttons = []
        for index, ch_name in enumerate(CHANNELS, 1):
            clean_ch = ch_name.replace('@', '')
            buttons.append([InlineKeyboardButton(f"📢 بەشداربە لە کەناڵی {index}", url=f"https://t.me/{clean_ch}")])
        
        buttons.append([InlineKeyboardButton("🔄 پشکنینی بەشداربوونی ئینفینیتی", callback_data="check_sub")])
        buttons.append([InlineKeyboardButton("👑 پەیوەندی بە خاوەن: @X_MAM6", url="https://t.me/X_MAM6")])
        keyboard = InlineKeyboardMarkup(buttons)
        
        await message.reply_text(
            "❌ تکایە سەرەتا لە هەموو کەناڵەکان بەشدار ببە تاوەکو سیستەمێ خاوەن @X_MAM6 ڕێگەی داونلۆدکرنێ بدات!\n\n"
            "👑 خاوەن: @X_MAM6",
            reply_markup=keyboard
        )
        return

    url_link = message.text.strip()
    if not url_link.startswith("http"):
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 خاوەن: @X_MAM6", url="https://t.me/X_MAM6")]
        ])
        await message.reply_text(
            "⚠️ تکایە لینکەکی دروست و ڕاستەقینە بنێرە برا!\n\n"
            "👑 خاوەن: @X_MAM6",
            reply_markup=err_kb
        )
        return

    process_msg = await message.reply_text(
        "⚡️ سیستەمێ ئینفینیتی: خەریکە زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n"
        "👑 خاوەن: @X_MAM6"
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
                InlineKeyboardButton("👑 خاوەن: @X_MAM6", url="https://t.me/X_MAM6")
            ]
        ])
        
        await process_msg.edit_text(
            f"🎬 ناڤێ ڤیدیۆیێ: {vid_title}\n"
            f"⏱ دەم: {vid_time} چرکە\n\n"
            "کوالیتیا خۆ هەڵبژێرە بۆ داونلۆدکرنێ 👇\n\n"
            "👑 خاوەن و بەرپرس: @X_MAM6",
            reply_markup=action_kb
        )
    except Exception as err:
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 خاوەن: @X_MAM6", url="https://t.me/X_MAM6")]
        ])
        await process_msg.edit_text(
            f"❌ هەڵەیەک ڕوویدا لە وەرگرتنی ڤیدیۆکە:\n`{str(err)}`\n\n"
            "👑 خاوەن: @X_MAM6",
            reply_markup=err_kb
        )

print("🚀 Infinity Supreme Bot with Owner @X_MAM6 is Running!")
app.run()
