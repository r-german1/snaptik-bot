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
    "mx_download_trillion_v99",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=5000,
    sleep_threshold=0
)

user_stats = {}
global_total_downloads = 0
banned_users = set()
secret_code_usage_count = {}

# 80 Distinct Secret Codes (600 Balance each, 2 users limit per code)
MX_80_CODES = {}
for i in range(1, 81):
    c_str = f"MX-TRL-9999-{i:03d}-{random.randint(1000, 9999)}"
    MX_80_CODES[c_str] = 600

for code in MX_80_CODES:
    secret_code_usage_count[code] = set()

def get_baghdad_time():
    t_sec = time.time() + 10800  # UTC+3 Baghdad
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t_sec))

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 پروفایلا من (ID & Specs)", callback_data="my_profile"),
            InlineKeyboardButton("📥 ڤیدیۆیێن داونلۆدکری", callback_data="my_downloads")
        ],
        [
            InlineKeyboardButton("📥 MX DOWNLOAD (No Watermark 165FPS)", callback_data="mx_video_download_menu"),
            InlineKeyboardButton("🎁 خەلاتێن 4 ساعتی (10 Key)", callback_data="legend_mx_claim")
        ],
        [
            InlineKeyboardButton("📢 چەنەلا مە (LEGEND_MODS33)", url="https://t.me/LEGEND_MODS33"),
            InlineKeyboardButton("🏆 Top 25 Downloaders", callback_data="top_25_ranking")
        ],
        [
            InlineKeyboardButton("📊 ئامارێن گشتی یێن بۆتی", callback_data="bot_global_stats"),
            InlineKeyboardButton("💡 ڕێنمایێن بەکارهۆنانێ", callback_data="bot_help")
        ],
        [
            InlineKeyboardButton("⚙️ سیستەم و پشکنین (120-165 FPS)", callback_data="system_status"),
            InlineKeyboardButton("🔄 نووکرنا سەرەکی (Refresh)", callback_data="refresh_home")
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
            "last_claim_time": 0, "last_daily_time": 0, "profile_id": f"MX-PID-{random.randint(100000, 999999)}",
            "mobile_type": "Android/iOS Trillion Engine (165FPS)", "daily_code": unique_daily_code,
            "claimed_secret_codes": set()
        }

    current_bal = user_stats[user_id]['balance']
    
    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ هێزدارترین سیستەمێ **MX DOWNLOAD** (9999K Trillion Server)!\n"
        "📢 سەرەدانا چەنەلا مە بکە بۆ وەرگرتنا 75 کۆدێن Balance یێن 600:\n"
        "🔗 https://t.me/LEGEND_MODS33\n\n"
        f"💰 Balance-ێ تە یێ نها: `{current_bal}` Key\n"
        f"⏰ دەمژمێرا بغداد: `{get_baghdad_time()}`\n\n"
        "🔗 لینکا خۆ (TikTok/Instagram/YouTube بێ واتەمارک) ل ڤێرە بنێرە!"
    )
    await message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^refresh_home$"))
async def refresh_home_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bal = user_stats.setdefault(user_id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🔄 **MX DOWNLOAD ب سەرکەفتن هاتە نووکرن!**\n\n💰 Balance-ێ تە: `{bal}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_main_menu_keyboard()
    )
    await callback_query.answer("🔄 نوو بوو!")

@app.on_callback_query(filters.regex(r"^mx_video_download_menu$"))
async def mx_video_download_menu_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_stats.setdefault(user_id, {"balance": 0})
    bal = user_stats[user_id]["balance"]
    menu_text = (
        "📥 **MX DOWNLOAD Lab (No Watermark - 165FPS Trillion):**\n\n"
        f"💰 Balance-ێ تە: `{bal}` Key\n"
        "✨ پشتەڤانیا YouTube, TikTok (No Watermark), Instagram (No Watermark).\n"
        "🚀 سێرڤەرێن 120FPS تا 165FPS بێ لادان و بێ خەلەتی.\n\n"
        "🔗 لینکا خۆ ل ڤێرە بنێرە بۆ داونلۆدکرنێ!"
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
        f"🎁 **پیرۆزە! +10 Key (خەلاتێ 4 ساعتی) هاتە زێدەکرن!**\n💰 Balance: `{stats['balance']}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer("🎉 10 Key هاتنە وەرگرتن!")

@app.on_callback_query(filters.regex(r"^my_profile$"))
async def profile_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.setdefault(user_id, {
        "balance": 0, "links_count": 0, "downloads_count": 0, "downloaded_videos": [],
        "profile_id": f"MX-PID-{random.randint(100000, 999999)}", "mobile_type": "Android/iOS Trillion Engine (165FPS)"
    })
    
    profile_text = (
        f"👤 **پروفایلا پێشکەفتیا تە (MX Profile):**\n\n"
        f"🔹 ناڤ: `{callback_query.from_user.first_name}`\n"
        f"🆔 User ID: `{user_id}`\n"
        f"🏷 Username: `{'@' + callback_query.from_user.username if callback_query.from_user.username else 'نەدیار'}`\n"
        f"📌 Profile ID: `{stats['profile_id']}`\n"
        f"📱 جۆرێ مۆبایلی / سیستەم: `{stats['mobile_type']}`\n"
        f"⏱ دەمژمێرا بغداد: `{get_baghdad_time()}`\n"
        f"• 💰 Balance: `{stats['balance']}` Key\n"
        f"• 📥 گشتی داونلۆد: `{stats['downloads_count']}`\n"
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
        f"📥 **دووماهیک داونلۆدێن MX (No Watermark):**\n"
        f"{vids_text}\n\n"
        f"📊 گشتی داونلۆد: `{stats['downloads_count']}`\n"
        f"💰 Balance: `{stats['balance']}` Key\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`"
    )
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^top_25_ranking$"))
async def top_25_ranking_handler(client, callback_query: CallbackQuery):
    sorted_users = sorted(user_stats.items(), key=lambda x: x[1].get("downloads_count", 0), reverse=True)[:25]
    
    top_text = "🏆 **ڕێزبەندا Top 25 (MX DOWNLOAD Trillion):**\n\n"
    if not sorted_users:
        top_text += "هێشتا کەس نەهاتیە ڕێزبەندێ."
    else:
        for idx, (uid, data) in enumerate(sorted_users, 1):
            name = data.get("name", "User")
            d_count = data.get("downloads_count", 0)
            top_text += f"{idx}. {name} — 📥 `{d_count}` ڤیدیۆ\n"
            
    top_text += f"\n⏰ وقت بغداد: `{get_baghdad_time()}`"
    await callback_query.message.edit_text(top_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_global_stats$"))
async def global_stats_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    await callback_query.message.edit_text(
        f"📊 **ئامارێن گشتی یێن MX DOWNLOAD:**\n"
        f"👥 کۆما کاربەران: `{len(user_stats)}`\n"
        f"📥 گشتی داونلۆدێن بۆتی: `{global_total_downloads}`\n"
        f"🌐 سەروەر: `Trillion 9999K (120-165 FPS)`\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_help$"))
async def bot_help_handler(client, callback_query: CallbackQuery):
    await callback_help_text = (
        "💡 **رێنمایێن بەکارهۆنانێ (MX DOWNLOAD):**\n"
        "• 80 کۆدێن ڤەشارتى (600 Key) ل چەنەلا `LEGEND_MODS33` هەنە (هەر کۆدەک بۆ 2 کەسانە).\n"
        "• هەر دابەزاندنەک تنێ 1 Key ژ تە دبرێت!\n"
        "• داونلۆدکرنا بێ واتەمارک بۆ TikTok و Instagram و YouTube.\n"
        "• سێرڤەرێن 120FPS تا 165FPS بێ کێشە و بێ لادان.\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`"
    )
    await callback_query.message.edit_text(callback_help_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^system_status$"))
async def system_status_handler(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "⚙️ **ڕاپۆرت و پشکنینا سیستەمی:**\n"
        "• سەروەرێ Trillion: `Active (9999K)`\n"
        "• فریم ڕەیت: `120 FPS - 165 FPS Ultra Smooth`\n"
        "• لادانا کێشەیێن Lag و Network: `Fixed & Optimized`\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^back_home$"))
async def back_home_handler(client, callback_query: CallbackQuery):
    bal = user_stats.setdefault(client, {}).get(callback_query.from_user.id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🌟 بخێرهاتن ڤە بۆ MX DOWNLOAD!\n💰 Balance-ێ تە: `{bal}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`",
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
        "last_claim_time": 0, "profile_id": f"MX-PID-{random.randint(100000, 999999)}",
        "mobile_type": "Android/iOS Trillion Engine (165FPS)",
        "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}",
        "last_daily_time": 0, "claimed_secret_codes": set()
    })

    if text_input in MX_80_CODES:
        if text_input in stats["claimed_secret_codes"] or user_id in secret_code_usage_count[text_input]:
            await message.reply_text(f"❌ تو ڤی کۆدی پێشتر وەرگرتیە!\n⏰ وقت بغداد: `{get_baghdad_time()}`")
            return
        if len(secret_code_usage_count[text_input]) >= 2:
            await message.reply_text(f"❌ سنوورێ ڤی کۆدی تەواو بوو (تنێ 2 کەس).\n⏰ وقت بغداد: `{get_baghdad_time()}`")
            return

        secret_code_usage_count[text_input].add(user_id)
        stats["claimed_secret_codes"].add(text_input)
        stats["balance"] += 600
        await message.reply_text(
            f"🎉 **پیرۆزە! +600 Balance (کۆدێ MX 80) هاتە زێدەکرن!**\n"
            f"💰 Balance-ێ نوو: `{stats['balance']}` Key\n"
            f"⏰ وقت بغداد: `{get_baghdad_time()}`"
        )
        return

    if text_input == stats["daily_code"]:
        if time.time() - stats["last_daily_time"] < 86400:
            await message.reply_text(f"⏳ کۆدێ ڕۆژانە تنێ جارەکێ د 24 دەمژمێران دا کاردکەت!\n⏰ وقت بغداد: `{get_baghdad_time()}`")
            return
        stats["last_daily_time"] = time.time()
        stats["balance"] += 75
        await message.reply_text(
            f"🎁 **+75 Key هاتە زێدەکرن!**\n"
            f"💰 Balance-ێ نوو: `{stats['balance']}` Key\n"
            f"⏰ وقت بغداد: `{get_baghdad_time()}`"
        )
        return

    if not text_input.startswith("http"):
        await message.reply_text(f"⚠️ ژکەرەما خۆ لینکا دروست (YouTube, TikTok, Instagram) یان کۆدەکێ ڕاست بنێرە!\n⏰ وقت بغداد: `{get_baghdad_time()}`")
        return

    if stats["balance"] < 1:
        await message.reply_text(f"❌ Balance-ێ تە کێمە! پێدڤییە حداقل 1 Key هەبت بۆ داونلۆدکرنێ.\n⏰ وقت بغداد: `{get_baghdad_time()}`")
        return

    stats["links_count"] += 1
    process_msg = await message.reply_text(f"⚡️ MX DOWNLOAD (9999K Server - 165FPS) خەریکە زانیاریان ئینیت خوارێ...\n⏰ وقت بغداد: `{get_baghdad_time()}`")

    try:
        ydl_opts = {'quiet': True, 'format': 'best', 'extractor_args': {'youtube': {'player_client': ['android', 'web']}}}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text_input, download=False)
            title = info.get('title', 'MX Trillion Media')

        action_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 MP4 (No Watermark - 1 Key)", callback_data=f"dl_mp4|{text_input}"), InlineKeyboardButton("🎵 MP3 (1 Key)", callback_data=f"dl_mp3_full|{text_input}")],
            [InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]
        ])
        await process_msg.edit_text(
            f"🎬 ناڤ: {title}\n"
            f"💰 Balance: `{stats['balance']}` Key (نرخ: 1 Key)\n"
            f"🚀 کواليتى: 165 FPS Ultra Smooth (No Watermark)\n\n"
            f"کوالیتیا خۆ هەڵبژێرە 👇\n⏰ وقت بغداد: `{get_baghdad_time()}`",
            reply_markup=action_kb
        )
    except Exception as e:
        await process_msg.edit_text(f"❌ هەڵە د ئینانا زانیاریان دا:\n`{str(e)}`\n⏰ وقت بغداد: `{get_baghdad_time()}`")

@app.on_callback_query(filters.regex(r"^dl_"))
async def download_callback_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    user_id = callback_query.from_user.id
    action, url_link = callback_query.data.split("|", 1)
    stats = user_stats.setdefault(user_id, {"balance": 0, "downloads_count": 0, "downloaded_videos": []})
    
    if stats["balance"] < 1:
        await callback_query.answer("❌ Balance-ێ تە نینە! (1 Key پێدڤییە)", show_alert=True)
        return

    stats["balance"] -= 1
    status_msg = await callback_query.message.reply_text(
        f"⏳ MX DOWNLOAD (165FPS Trillion Engine) خەریکە دابەزینت (No Watermark)...\n"
        f"💰 Balance-ێ مایی: `{stats['balance']}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`"
    )
    
    filename = None
    try:
        os.makedirs("downloads", exist_ok=True)
        if action == "dl_mp4":
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best', 'merge_output_format': 'mp4',
                'outtmpl': 'downloads/%(id)s.%(ext)s', 'quiet': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_link, download=True)
                filename = ydl.prepare_filename(info)
                if not filename.endswith('.mp4'):
                    filename = os.path.splitext(filename)[0] + '.mp4'
                title = info.get('title', 'MX Video')
            await callback_query.message.reply_video(
                video=filename,
                caption=f"🎬 MP4 (No Watermark - 165FPS) هاتە داونلۆدکرن!\n💰 Balance: `{stats['balance']}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`"
            )
        else:
            ydl_opts = {
                'format': 'bestaudio/best', 'outtmpl': 'downloads/%(id)s.%(ext)s', 'quiet': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_link, download=True)
                filename = ydl.prepare_filename(info)
                title = info.get('title', 'MX Audio')
            await callback_query.message.reply_audio(
                audio=filename, title=title, performer="MX Trillion",
                caption=f"🎶 MP3 هاتە داونلۆدکرن!\n💰 Balance: `{stats['balance']}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`"
            )

        stats["downloads_count"] += 1
        global_total_downloads += 1
        stats["downloaded_videos"].append(title[:30])
        
        if filename and os.path.exists(filename):
            os.remove(filename)
        await status_msg.delete()
    except Exception as e:
        stats["balance"] += 1  # Refund Key on error
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        await status_msg.edit_text(f"❌ هەڵە د دابەزاندنێ دا (Key هاتە ڤەگەراندن):\n`{str(e)}`\n⏰ وقت بغداد: `{get_baghdad_time()}`")

app.run()
