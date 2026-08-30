import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")

OWNER_USERNAME = "@YUSEEF_SURCHI"
CHANNELS = [
    "@KurdishCinemas"
]

app = Client(
    "infinity_supreme_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=800,
    sleep_threshold=2
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
            buttons.append([InlineKeyboardButton("📢 بەشداربە لە کەناڵی KurdishCinemas", url=f"https://t.me/{clean_ch}")])
        
        buttons.append([InlineKeyboardButton("🔄 پشکنینا بەشداربوونێ", callback_data="check_sub")])
        buttons.append([InlineKeyboardButton(f"👑 پەیوەندی ب خودان: {OWNER_USERNAME}", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")])
        keyboard = InlineKeyboardMarkup(buttons)
        
        await message.reply_text(
            f"⚠️ هایداربە ل سیستەمێ خودان {OWNER_USERNAME}:\n\n"
            f"بۆ وێ چەندێ تو بکاری ژ ڤێ بۆتا بێ سنور کەلکێ وەربگری، هیڤیە پێش هەمی تشتکی تو ل کەناڵی KurdishCinemas بەشدار ببەی!\n\n"
            f"پشتی بەشداربوونێ، دوگمەیا پشکنینێ کلیک بکە 👇\n\n"
            f"👑 خودان: {OWNER_USERNAME}",
            reply_markup=keyboard
        )
        return

    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست!\n\n"
        f"🤖 ئەڤە مەزنترین و پێشکەفتنترین بۆتا داونلۆدکرنێ یە ل جیهانێ، کو کوالیتیا 4K و MP3 بێ کێشە بۆ تە دئینە خوارێ.\n\n"
        f"👑 خودان و دامەزرێنەرێ ڕەها یێ ئەڤێ بۆتێ: {OWNER_USERNAME}\n\n"
        f"🔗 بۆ دەستپێکرنێ، لینکێ ڤیدیۆیا خۆ (تیکتۆک، اینستاگرام، یوتیوب، سناپچات) بۆ من بنێرە بۆ داونلۆدکرنێ!"
    )
    
    welcome_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"👑 خودان: {OWNER_USERNAME}", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")]
    ])
    await message.reply_text(welcome_text, reply_markup=welcome_kb)

@app.on_callback_query(filters.regex("check_sub"))
async def callback_check_subscription(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    is_joined = await check_all_channels(client, user_id)
    
    if not is_joined:
        await callback_query.answer(f"❌ هێشتا تو ل کەناڵی KurdishCinemas بەشدار نەکری یی!\n👑 خودان: {OWNER_USERNAME}", show_alert=True)
        return
    
    await callback_query.answer(f"✅ پیرۆزە! نوکە تو دکاری ڤیدیۆیان بۆ من بنێری.\n👑 خودان: {OWNER_USERNAME}", show_alert=True)
    
    success_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"👑 خودان: {OWNER_USERNAME}", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")]
    ])
    
    await callback_query.message.edit_text(
        f"🌟 **سوپاس بۆ بەشداربوونا تە ل کەناڵی KurdishCinemas!**\n\n"
        f"🤖 نوکە بۆتا مە ئامادەیە. لینکێ ڤیدیۆیا خۆ (تیکتۆک، اینستاگرام، یوتیوب، سناپچات) بۆ من بنێرە!\n\n"
        f"👑 خودان و بەرپرس: {OWNER_USERNAME}",
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
            buttons.append([InlineKeyboardButton("📢 بەشداربە لە کەناڵی KurdishCinemas", url=f"https://t.me/{clean_ch}")])
        
        buttons.append([InlineKeyboardButton("🔄 پشکنینا بەشداربوونێ", callback_data="check_sub")])
        buttons.append([InlineKeyboardButton(f"👑 پەیوەندی ب خودان: {OWNER_USERNAME}", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")])
        keyboard = InlineKeyboardMarkup(buttons)
        
        await message.reply_text(
            f"❌ هیڤیە پێش هەمی تشتکی تو ل کەناڵی KurdishCinemas بەشدار ببە دا سیستەمێ خودان {OWNER_USERNAME} ڕێکا داونلۆدکرنێ بدەتە تە!\n\n"
            f"👑 خودان: {OWNER_USERNAME}",
            reply_markup=keyboard
        )
        return

    url_link = message.text.strip()
    if not url_link.startswith("http"):
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"👑 خودان: {OWNER_USERNAME}", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")]
        ])
        await message.reply_text(
            f"⚠️ هیڤیە لینکەکا دروست و ڕاستەقینە بۆ من بنێرە برا!\n\n"
            f"👑 خودان: {OWNER_USERNAME}",
            reply_markup=err_kb
        )
        return

    process_msg = await message.reply_text(
        f"⚡️ سیستەمێ ئەسینا (ب 800 سێرڤەران): نوکە زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n"
        f"👑 خودان: {OWNER_USERNAME}"
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
                InlineKeyboardButton(f"👑 خودان: {OWNER_USERNAME}", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")
            ]
        ])
        
        await process_msg.edit_text(
            f"🎬 ناڤێ ڤیدیۆیێ: {vid_title}\n"
            f"⏱ دەم: {vid_time} چرکه\n\n"
            f"کوالیتیا خۆ هەڵبژێرە بۆ داونلۆدکرنێ 👇\n\n"
            f"👑 خودان و بەرپرس: {OWNER_USERNAME}",
            reply_markup=action_kb
        )
    except Exception as err:
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"👑 خودان: {OWNER_USERNAME}", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")]
        ])
        await process_msg.edit_text(
            f"❌ هەڵەیەک ڕوویدا د وەرگرتنا ڤیدیۆیێ دا:\n`{str(err)}`\n\n"
            f"👑 خودان: {OWNER_USERNAME}",
            reply_markup=err_kb
        )

print(f"🚀 High-Performance Infinity Supreme Bot with 800 Workers and Owner {OWNER_USERNAME} is Running!")
app.run()
