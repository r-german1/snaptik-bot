import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")
OWNER_USERNAME = "@X_MAM6"

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
        keyboard = InlineKeyboardMarkup(buttons)
        
        await message.reply_text(
            f"⚠️ ئاگاداری لە سیستەمی خاوەن {OWNER_USERNAME}:\n\n"
            f"بۆ ئەوەی بتوانیت لەم بۆتە بێسنوورە کەڵک وەربگریت، دەبێت سەرەتا لە هەموو ئەم کەناڵانەی خوارەوە بەشدار ببیت!\n\n"
            f"پشتی بەشداربوون، دوگمەی پشکنین کلیک بکە 👇",
            reply_markup=keyboard
        )
        return

    welcome_text = (
        f"🌟 سڵاو لە تو هەڤاڵی خۆشەویست!\n\n"
        f"🤖 ئەمە مەزنترین و پێشکەوتووترین بۆتی داونلۆدکردنی جیهانە بێ هیچ سنوورەکێ کو کوالیتیا 4K و MP3 بێ کێشە پێشکەش دکەت.\n\n"
        f"👑 خاوەن و دامەزرێنەری ڕەهای ئەم بۆتە: {OWNER_USERNAME}\n\n"
        f"🔗 بۆ دەستپێکردن، لینکەی ڤیدیۆکەی (تیکتۆک، اینستاگرام، یوتیوب، سناپچات) بنێرە بۆم بۆ داونلۆدکرنێ!"
    )
    await message.reply_text(welcome_text)

# **بەشا نوی و گرنگ بۆ چارەسەرکرنا دوگمەی پشکنینێ:**
@app.on_callback_query(filters.regex("check_sub"))
async def callback_check_subscription(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    is_joined = await check_all_channels(client, user_id)
    
    if not is_joined:
        await callback_query.answer("❌ هێشتا لە هەموو کەناڵەکان بەشدار نەکردوویت!", show_alert=True)
        return
    
    await callback_query.answer("✅ پیرۆزە! ئێستا دەتوانیت ڤیدیۆ بنێریت.", show_alert=True)
    await callback_query.message.edit_text(
        f"🌟 **سوپاس بۆ بەشداربوونا تە ل هەمی کەناڵان!**\n\n"
        f"🤖 ئێستا بۆتەکەی مە ئامادەیە. لینکەی ڤیدیۆیا خۆ (تیکتۆک، اینستاگرام، یوتیوب، سناپچات) بنێرە بۆم!\n\n"
        f"👑 خاوەن: {OWNER_USERNAME}"
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
        keyboard = InlineKeyboardMarkup(buttons)
        
        await message.reply_text(
            f"❌ تکایە سەرەتا لە هەموو کەناڵەکان بەشدار ببە تاوەکو سیستەمێ خاوەن {OWNER_USERNAME} ڕێگەی داونلۆدکرنێ بدات!",
            reply_markup=keyboard
        )
        return

    url_link = message.text.strip()
    if not url_link.startswith("http"):
        await message.reply_text(f"⚠️ تکایە لینکەکی دروست و ڕاستەقینە بنێرە برا!\n\n👑 خاوەن: {OWNER_USERNAME}")
        return

    process_msg = await message.reply_text(f"⚡️ سیستەمێ ئینفینیتی: خەریکە زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n👑 خاوەن: {OWNER_USERNAME}")

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
                InlineKeyboardButton(f"👑 خاوەن: {OWNER_USERNAME}", url="https://t.me/X_MAM6")
            ]
        ])
        
        await process_msg.edit_text(
            f"🎬 ناڤێ ڤیدیۆیێ: {vid_title}\n"
            f"⏱ دەم: {vid_time} چرکە\n\n"
            f"کوالیتیا خۆ هەڵبژێرە بۆ داونلۆدکرنێ 👇\n\n"
            f"👑 خاوەن و بەرپرس: {OWNER_USERNAME}",
            reply_markup=action_kb
        )
    except Exception as err:
        await process_msg.edit_text(
            f"❌ هەڵەیەک ڕوویدا لە وەرگرتنی ڤیدیۆکە:\n`{str(err)}`\n\n"
            f"👑 خاوەن: {OWNER_USERNAME}"
        )

print("🚀 Infinity Supreme Bot with Working Callback is Running!")
app.run()
