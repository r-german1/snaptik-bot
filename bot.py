import os
import asyncio
import time
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")
REQUIRED_CHANNEL = "LEGEND_MODS33"

app = Client(
    "mx_download_ultimate_v80",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    sleep_threshold=0
)

user_stats = {}
global_total_downloads = 0
banned_users = set()
secret_code_usage_count = {}

# 80 Secret Codes Generation
MX_80_SECRET_CODES = {}
for i in range(1, 81):
    code_str = f"MX-SECRET-{i:03d}-{random.randint(1000, 9999)}"
    MX_80_SECRET_CODES[code_str] = 600

for code in MX_80_SECRET_CODES:
    secret_code_usage_count[code] = set()

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 پروفایلا پێشکەفتى", callback_data="my_profile"),
            InlineKeyboardButton("📥 ڤیدیۆیێن داونلۆدکری", callback_data="my_downloads")
        ],
        [
            InlineKeyboardButton("📥 MX DOWNLOAD (No Watermark)", callback_data="mx_video_download_menu"),
            InlineKeyboardButton("🎁 خەلاتێن 4 ساعتی (10 Key)", callback_data="legend_mx_claim")
        ],
        [
            InlineKeyboardButton("🏆 Top 25 Downloaders", callback_data="top_25_ranking"),
            InlineKeyboardButton("📊 ئامارێن گشتی یێن بۆتی", callback_data="bot_global_stats")
        ],
        [
            InlineKeyboardButton("💡 رێنمایێن بەکارهۆنانێ", callback_data="bot_help"),
            InlineKeyboardButton("⚙️ سیستەم و پشکنین", callback_data="system_status")
        ],
        [
            InlineKeyboardButton("🔄 نووکرنا سەرەکی (Refresh)", callback_data="refresh_home"),
            InlineKeyboardButton("👑 @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
        ]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_home"), InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")]
    ])

@app.on_message(filters.command("start"))
async def start_command_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.reply_text("❌ لێبوورین، تو هاتیە بلۆککرن.")
        return

    user_name = message.from_user.first_name or "User"
    user_username = f"@{message.from_user.username}" if message.from_user.username else "نەدیار"

    if user_id not in user_stats:
        unique_daily_code = f"MX-DAY-{user_id}-{random.randint(1000, 9999)}"
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0,
            "downloads_count": 0, "downloaded_videos": [], "balance": 0,
            "last_claim_time": 0, "last_daily_time": 0,
            "daily_code": unique_daily_code, "claimed_secret_codes": set()
        }

    current_bal = user_stats[user_id]['balance']
    
    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ **MX DOWNLOAD**!\n"
        "📢 80 کۆدێن نوو یێن ڤەشارتى (600 Key) ل چەنەلا مە هەنە:\n"
        "🔗 https://t.me/LEGEND_MODS33\n\n"
        f"💰 Balance-ێ تە یێ نها: `{current_bal}` Key\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دابەزاندنێ (YouTube, TikTok, Instagram بێ واتەمارک)، لینکێ خۆ ل ڤێرە بنێرە!"
    )
    await message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^refresh_home$"))
async def refresh_home_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bal = user_stats.setdefault(user_id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🔄 **MX DOWNLOAD نوو بوو!**\n\n💰 Balance-ێ تە: `{bal}` Key\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=get_main_menu_keyboard()
    )
    await callback_query.answer("🔄 نوو بوو!")

@app.on_callback_query(filters.regex(r"^mx_video_download_menu$"))
async def mx_video_download_menu_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_stats.setdefault(user_id, {"balance": 0})
    bal = user_stats[user_id]["balance"]
    menu_text = (
        "📥 **MX DOWNLOAD (No Watermark Lab):**\n\n"
        f"💰 Balance-ێ تە: `{bal}` Key\n\n"
        "✨ پشتەڤانیا YouTube, TikTok (No Watermark), Instagram (No Watermark) دکەت.\n"
        "🔗 لینکا خۆ ل ڤێرە بنێرە!\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    await callback_query.message.edit_text(menu_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^legend_mx_claim$"))
async def legend_mx_claim_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    current_t = time.time()
    stats = user_stats.setdefault(user_id, {"balance": 0, "last_claim_time": 0, "downloads_count": 0, "downloaded_videos": []})
    
    if current_t - stats["last_claim_time"] < 14400:
        remaining = int(14400 - (current_t - stats["last_claim_time"]))
        hours = remaining // 3600
        mins = (remaining % 3600) // 60
        await callback_query.answer(f"⏳ چاڤەڕێی {hours} دەمژمێر و {mins} خولەکان بن.", show_alert=True)
        return
        
    stats["last_claim_time"] = current_t
    stats["balance"] += 10
    await callback_query.message.edit_text(
        f"🎁 **پیرۆزە! +10 Key هاتە زێدەکرن!**\n💰 Balance: `{stats['balance']}` Key\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer("🎉 10 Key هاتنە وەرگرتن!")

@app.on_callback_query(filters.regex(r"^my_profile$"))
async def profile_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.setdefault(user_id, {"balance": 0, "links_count": 0, "downloads_count": 0, "downloaded_videos": [], "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}"})
    profile_text = (
        f"👤 **پروفایلا تە ل MX DOWNLOAD:**\n\n"
        f"🔹 ناڤ: `{callback_query.from_user.first_name}`\n"
        f"• 💰 Balance: `{stats['balance']}` Key\n"
        f"• 📥 گشتی داونلۆد: `{stats['downloads_count']}`\n"
        f"• 🎁 کۆدێ تایبەتێ ڕۆژانە: `{stats['daily_code']}`\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    await callback_query.message.edit_text(profile_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^my_downloads$"))
async def downloads_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.get(user_id, {"downloads_count": 0, "downloaded_videos": [], "balance": 0})
    vids = stats.get("downloaded_videos", [])
    
    vids_text = "\n".join([f"• {v}" for v in vids[-10:]]) if vids else "هیچ ڤیدیۆیەک نەهاتیە داونلۆدکرن."
    
    text = (
        f"📥 **دووماهیک داونلۆدێن MX:**\n"
        f"{vids_text}\n\n"
        f"📊 گشتی داونلۆد: `{stats['downloads_count']}`\n"
        f"💰 Balance: `{stats['balance']}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^top_25_ranking$"))
async def top_25_ranking_handler(client, callback_query: CallbackQuery):
    sorted_users = sorted(user_stats.items(), key=lambda x: x[1].get("downloads_count", 0), reverse=True)[:25]
    
    top_text = "🏆 **ڕێزبەندا Top 25 (MX DOWNLOAD):**\n\n"
    if not sorted_users:
        top_text += "هێشتا کەس نەهاتیە ڕێزبەندێ."
    else:
        for idx, (uid, data) in enumerate(sorted_users, 1):
            name = data.get("name", "User")
            d_count = data.get("downloads_count", 0)
            top_text += f"{idx}. {name} — 📥 `{d_count}` ڤیدیۆ\n"
            
    top_text += "\n👑 خودان: @YUSEEF_SURCHI"
    await callback_query.message.edit_text(top_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_global_stats$"))
async def global_stats_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    await callback_query.message.edit_text(
        f"📊 **ئامارێن گشتی یێن MX DOWNLOAD:**\n"
        f"👥 کاربەر: `{len(user_stats)}`\n"
        f"📥 گشتی داونلۆد: `{global_total_downloads}`\n\n"
        "👑 خودان: @YUSEEF_SURCHI",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_help$"))
async def bot_help_handler(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "💡 **رێنمایێن بەکارهۆنانێ:**\n"
        "• 80 کۆدێن ڤەشارتى (600 Key) ل چەنەلا `LEGEND_MODS33` هەنە.\n"
        "• داونلۆدکرنا بێ واتەمارک بۆ TikTok و Instagram.\n"
        "• هەلبژارتنا MP4 و MP3.\n\n"
        "👑 خودان: @YUSEEF_SURCHI",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^system_status$"))
async def system_status_handler(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "⚙️ **سیستەمێ MX DOWNLOAD ب تەواوی چالاك و ب ڕێکوپێکی کار دکەت.**\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^back_home$"))
async def back_home_handler(client, callback_query: CallbackQuery):
    bal = user_stats.setdefault(callback_query.from_user.id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🌟 بخێرهاتن ڤە!\n💰 Balance-ێ تە: `{bal}` Key\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=get_main_menu_keyboard()
    )
    await callback_query.answer()

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def downloader_core_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        return

    text_input = message.text.strip()
    stats = user_stats.setdefault(user_id, {
        "balance": 0, "links_count": 0, "downloads_count": 0,
        "success_count": 0, "downloaded_videos": [], "name": message.from_user.first_name or "User",
        "last_claim_time": 0, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}",
        "last_daily_time": 0, "claimed_secret_codes": set()
    })

    if text_input in MX_80_SECRET_CODES:
        if text_input in stats["claimed_secret_codes"] or user_id in secret_code_usage_count[text_input]:
            await message.reply_text("❌ تو ڤی کۆدی پێشتر وەرگرتیە!\n\n👑 خودان: @YUSEEF_SURCHI")
            return
        if len(secret_code_usage_count[text_input]) >= 2:
            await message.reply_text("❌ سنوورێ ڤی کۆدی تەواو بوو (تنێ 2 کەس).\n\n👑 خودان: @YUSEEF_SURCHI")
            return

        secret_code_usage_count[text_input].add(user_id)
        stats["claimed_secret_codes"].add(text_input)
        stats["balance"] += 600
        await message.reply_text(
            f"🎉 **پیرۆزە! +600 Balance (کۆدێ MX 80) هاتە زێدەکرن!**\n💰 Balance-ێ نوو: `{stats['balance']}` Key\n\n👑 خودان: @YUSEEF_SURCHI"
        )
        return

    if text_input == stats["daily_code"]:
        if time.time() - stats["last_daily_time"] < 86400:
            await message.reply_text("⏳ کۆدێ ڕۆژانە تنێ جارەکێ د 24 دەمژمێران دا کاردکەت!")
            return
        stats["last_daily_time"] = time.time()
        stats["balance"] += 75
        await message.reply_text(
            f"🎁 **+75 Key هاتە زێدەکرن!**\n💰 Balance-ێ نوو: `{stats['balance']}` Key\n\n👑 خودان: @YUSEEF_SURCHI"
        )
        return

    if not text_input.startswith("http"):
        await message.reply_text("⚠️ ژکەرەما خۆ لینکا دروست (YouTube, TikTok, Instagram) یان کۆدەکێ ڕاست بنێرە!\n\n👑 خودان: @YUSEEF_SURCHI")
        return

    stats["links_count"] += 1
    process_msg = await message.reply_text("⚡️ MX DOWNLOAD خەریکە زانیاریان ئینیت خوارێ...\n\n👑 خودان: @YUSEEF_SURCHI")

    try:
        ydl_opts = {'quiet': True, 'format': 'best', 'extractor_args': {'youtube': {'player_client': ['android', 'web']}}}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text_input, download=False)
            title = info.get('title', 'MX Media Video')

        action_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 MP4 (No Watermark)", callback_data=f"dl_mp4|{text_input}"), InlineKeyboardButton("🎵 MP3", callback_data=f"dl_mp3_full|{text_input}")],
            [InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]
        ])
        await process_msg.edit_text(f"🎬 ناڤ: {title}\n💰 Balance: `{stats['balance']}` Key\n\nکوالیتیا خۆ هەڵبژێرە 👇\n\n👑 خودان: @YUSEEF_SURCHI", reply_markup=action_kb)
    except Exception as e:
        await process_msg.edit_text(f"❌ هەڵە د ئینانا زانیاریان دا: `{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI")

@app.on_callback_query(filters.regex(r"^dl_"))
async def download_callback_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    user_id = callback_query.from_user.id
    action, url_link = callback_query.data.split("|", 1)
    stats = user_stats.setdefault(user_id, {"balance": 0, "downloads_count": 0, "downloaded_videos": []})
    
    status_msg = await callback_query.message.reply_text(f"⏳ MX DOWNLOAD خەریکە دابەزینت (No Watermark)... \n\n👑 خودان: @YUSEEF_SURCHI")
    
    filename = None
    try:
        os.makedirs("downloads", exist_ok=True)
        if action == "dl_mp4":
            ydl_opts = {'format': 'bestvideo+bestaudio/best', 'merge_output_format': 'mp4', 'outtmpl': 'downloads/%(id)s.%(ext)s', 'quiet': True, 'extractor_args': {'youtube': {'player_client': ['android', 'web']}}}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_link, download=True)
                filename = ydl.prepare_filename(info)
                if not filename.endswith('.mp4'):
                    filename = os.path.splitext(filename)[0] + '.mp4'
                title = info.get('title', 'MX Video')
            await callback_query.message.reply_video(video=filename, caption=f"🎬 MP4 (No Watermark) هاتە داونلۆدکرن!\n\n👑 خودان: @YUSEEF_SURCHI")
        else:
            ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'downloads/%(id)s.%(ext)s', 'quiet': True, 'extractor_args': {'youtube': {'player_client': ['android', 'web']}}}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_link, download=True)
                filename = ydl.prepare_filename(info)
                title = info.get('title', 'MX Audio')
            await callback_query.message.reply_audio(audio=filename, title=title, performer="YUSEEF_SURCHI", caption=f"🎶 MP3 هاتە داونلۆدکرن!\n\n👑 خودان: @YUSEEF_SURCHI")

        stats["downloads_count"] += 1
        global_total_downloads += 1
        stats["downloaded_videos"].append(title[:30])
        
        if filename and os.path.exists(filename):
            os.remove(filename)
        await status_msg.delete()
    except Exception as e:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        await status_msg.edit_text(f"❌ هەڵە د دابەزاندنێ دا:\n`{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI")

app.run()
