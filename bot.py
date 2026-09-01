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
OWNER_USERNAME = "@LEGEND_MODS33"  # ناڤێ خودانی بۆ وەرگرتنا Free Key

app = Client(
    "mx_download_omega_supreme_god_2026",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=200000,
    sleep_threshold=0
)

user_stats = {}
global_total_downloads = 0
banned_users = set()
secret_code_usage_count = {}

# 80 Secret Codes (Each gives 1,000 Balance, strictly for 1 user max)
MX_80_CODES = {}
for i in range(1, 81):
    c_str = f"MX-SEC-1K-{i:02d}-{random.randint(100000, 999999)}"
    MX_80_CODES[c_str] = 1000

# 200 Massive Secret Codes (Each gives 10M Balance, strictly for 1 user max)
MX_200_CODES = {}
for i in range(1, 201):
    c_str = f"MX-ULTRA-10M-{i:03d}-{random.randint(100000, 999999)}"
    MX_200_CODES[c_str] = 10000000

# Combine all secret codes into a single dictionary
ALL_SECRET_CODES = {**MX_80_CODES, **MX_200_CODES}
for code in ALL_SECRET_CODES:
    secret_code_usage_count[code] = set()

def get_baghdad_time():
    t_sec = time.time() + 10800  # UTC+3 Baghdad Time
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t_sec))

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 پروفایلا من (Omega Specs)", callback_data="my_profile"),
            InlineKeyboardButton("📥 ڤیدیۆیێن داونلۆدکری", callback_data="my_downloads")
        ],
        [
            InlineKeyboardButton("📥 MX DOWNLOAD (720FPS Omega)", callback_data="mx_video_download_menu"),
            InlineKeyboardButton("🎁 خەلاتێ 4 دەمژمێری (10 Key)", callback_data="legend_mx_claim")
        ],
        [
            InlineKeyboardButton("💎 وەرگرتنا Free Key (سەرەدانا خودانی)", url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}"),
            InlineKeyboardButton("🏆 Top 100 Omega Ranking", callback_data="top_100_ranking")
        ],
        [
            InlineKeyboardButton("📢 چەنەلا مە (LEGEND_MODS33)", url="https://t.me/LEGEND_MODS33"),
            InlineKeyboardButton("📊 ئامارێن گشتی یێن بۆتی", callback_data="bot_global_stats")
        ],
        [
            InlineKeyboardButton("💡 ڕێنمایێن بەکارهۆنانێ", callback_data="bot_help"),
            InlineKeyboardButton("⚙️ سیستەم و پشکنین (720 FPS)", callback_data="system_status")
        ],
        [
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
        referral_link = f"https://t.me/{client.me.username}?start=ref_{user_id}"
        mobile_hint = "Omega Android / iOS God Device (720FPS)"
        if message.from_user.is_premium:
            mobile_hint = "Telegram Premium Omega Overlord Device"
            
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0,
            "downloads_count": 0, "downloaded_videos": [], "balance": 100,
            "last_claim_time": 0, 
            "profile_id": f"MX-PID-OMEGA-{random.randint(100000, 999999)}",
            "mobile_type": mobile_hint,
            "claimed_secret_codes": set(), "ref_link": referral_link,
            "ref_count": 0, "level": "Omega Novice", "xp": 0
        }

    current_bal = user_stats[user_id]['balance']
    
    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ **MX DOWNLOAD** (OMEGA SUPREME GOD 100M+ Engine)!\n"
        "📢 سەرەدانا چەنەلا مە بکە بۆ وەرگرتنا کۆدێن ڤەشارتی یێن 1K و 10M:\n"
        "🔗 https://t.me/LEGEND_MODS33\n\n"
        f"💰 Balance-ێ تە یێ نها: `{current_bal}` Key\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`\n\n"
        "🔗 لینکا خۆ (TikTok/Instagram/YouTube بێ واتەمارک) ل ڤێرە بنێرە!"
    )
    await message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^refresh_home$"))
async def refresh_home_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bal = user_stats.setdefault(user_id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🔄 **MX DOWNLOAD Omega ب سەرکەفتن هاتە نووکرن!**\n\n💰 Balance-ێ تە: `{bal}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_main_menu_keyboard()
    )
    await callback_query.answer("🔄 نوو بوو!")

@app.on_callback_query(filters.regex(r"^mx_video_download_menu$"))
async def mx_video_download_menu_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_stats.setdefault(user_id, {"balance": 0})
    bal = user_stats[user_id]["balance"]
    menu_text = (
        "📥 **MX DOWNLOAD Omega Lab (No Watermark - 720FPS):**\n\n"
        f"💰 Balance-ێ تە: `{bal}` Key\n"
        "✨ پشتەڤانیا تەواوا YouTube, TikTok (No Watermark), Instagram (No Watermark).\n"
        "🚀 نرخێ هەر داونلۆدەکێ: 1 Key\n\n"
        "🔗 لینکا خۆ ل ڤێرە بنێرە بۆ داونلۆدکرنێ!"
    )
    await callback_query.message.edit_text(menu_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^legend_mx_claim$"))
async def legend_mx_claim_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    current_t = time.time()
    stats = user_stats.setdefault(user_id, {"balance": 0, "last_claim_time": 0, "downloads_count": 0, "downloaded_videos": []})
    
    # 4 hours = 14400 seconds
    if current_t - stats["last_claim_time"] < 14400:
        remaining = int(14400 - (current_t - stats["last_claim_time"]))
        hours = remaining // 3600
        mins = (remaining % 3600) // 60
        secs = remaining % 60
        await callback_query.answer(f"⏳ چاڤەڕێی {hours} دەمژمێر، {mins} خولەک و {secs} چرکە بن.", show_alert=True)
        return
        
    stats["last_claim_time"] = current_t
    stats["balance"] += 10
    await callback_query.message.edit_text(
        f"🎁 **پیرۆزە! +10 Key (خەلاتێ 4 دەمژمێری) هاتە زێدەکرن!**\n💰 Balance: `{stats['balance']}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer("🎉 10 Key هاتنە وەرگرتن!")

@app.on_callback_query(filters.regex(r"^my_profile$"))
async def profile_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.setdefault(user_id, {
        "balance": 0, "links_count": 0, "downloads_count": 0, "downloaded_videos": [],
        "profile_id": f"MX-PID-OMEGA-{random.randint(100000, 999999)}", "mobile_type": "Omega Android/iOS Device (720FPS)",
        "level": "Omega Novice", "xp": 0, "ref_count": 0
    })
    
    profile_text = (
        f"👤 **پروفایلا Omega یا تە:**\n\n"
        f"🔹 ناڤ: `{callback_query.from_user.first_name}`\n"
        f"🆔 User ID: `{user_id}`\n"
        f"🏷 Username: `{'@' + callback_query.from_user.username if callback_query.from_user.username else 'نەدیار'}`\n"
        f"📌 Profile ID: `{stats['profile_id']}`\n"
        f"📱 جۆرێ مۆبایلی / سیستەم: `{stats['mobile_type']}`\n"
        f"⭐ پلە (Level): `{stats['level']}` (XP: {stats['xp']})\n"
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
        f"📥 **دووماهیک داونلۆدێن Omega (No Watermark):**\n"
        f"{vids_text}\n\n"
        f"📊 گشتی داونلۆد: `{stats['downloads_count']}`\n"
        f"💰 Balance: `{stats['balance']}` Key\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`"
    )
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^top_100_ranking$"))
async def top_100_ranking_handler(client, callback_query: CallbackQuery):
    sorted_users = sorted(user_stats.items(), key=lambda x: x[1].get("downloads_count", 0), reverse=True)[:100]
    
    top_text = "🏆 **ڕێزبەندا Top 100 (Omega Supreme):**\n\n"
    if not sorted_users:
        top_text += "هێشتا کەس نەهاتیە ڕێزبەندێ."
    else:
        for idx, (uid, data) in enumerate(sorted_users, 1):
            name = data.get("name", "User")
            d_count = data.get("downloads_count", 0)
            lvl = data.get("level", "Omega Novice")
            top_text += f"{idx}. {name} ({lvl}) — 📥 `{d_count}` ڤیدیۆ\n"
            
    top_text += f"\n⏰ وقت بغداد: `{get_baghdad_time()}`"
    await callback_query.message.edit_text(top_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_global_stats$"))
async def global_stats_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    await callback_query.message.edit_text(
        f"📊 **ئامارێن گشتی یێن MX Omega:**\n"
        f"👥 کۆما کاربەران: `{len(user_stats)}`\n"
        f"📥 گشتی داونلۆدێن بۆتی: `{global_total_downloads}`\n"
        f"🌐 سەروەر: `Omega Supreme God 100M+ Engine (720 FPS)`\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_help$"))
async def bot_help_handler(client, callback_query: CallbackQuery):
    help_text = (
        "💡 **رێنمایێن بەکارهۆنانێ (MX Omega Supreme God):**\n"
        "• 80 کۆدێن فەشارتی (هەر ئێشک 1,000 Key تنێ بۆ 1 کەس).\n"
        "• 200 کۆدێن زەبەلاح (هەر ئێشک 10M Key تنێ بۆ 1 کەس).\n"
        "• خەلاتێ 4 دەمژمێری 10 Key ددەت.\n"
        "• نرخێ هەر دابەزاندنەکێ 1 Key یە.\n"
        f"• بۆ وەرگرتنا Free Key سەرەدانا خودانی بکە: {OWNER_USERNAME}\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`"
    )
    await callback_query.message.edit_text(help_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^system_status$"))
async def system_status_handler(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "⚙️ **ڕاپۆرت و پشکنینا سیستەمی (Omega 100M+):**\n"
        "• سەروەرێ Omega Supreme: `Active (9999999K)`\n"
        "• فریم ڕەیت و کوالیتى: `720 FPS Hyper Quantum Smooth`\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^back_home$"))
async def back_home_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bal = user_stats.setdefault(user_id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🌟 بخێرهاتن ڤە بۆ MX DOWNLOAD Omega!\n💰 Balance-ێ تە: `{bal}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`",
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
        "balance": 100, "links_count": 0, "downloads_count": 0,
        "success_count": 0, "downloaded_videos": [], "name": message.from_user.first_name or "User",
        "last_claim_time": 0, "profile_id": f"MX-PID-OMEGA-{random.randint(100000, 999999)}",
        "mobile_type": "Omega Android/iOS Device (720FPS)",
        "claimed_secret_codes": set(),
        "level": "Omega Novice", "xp": 0, "ref_count": 0
    })

    if text_input in ALL_SECRET_CODES:
        if text_input in stats["claimed_secret_codes"] or user_id in secret_code_usage_count[text_input]:
            await message.reply_text(f"❌ تو ڤی کۆدی پێشتر وەرگرتیە!\n⏰ وقت بغداد: `{get_baghdad_time()}`")
            return
        if len(secret_code_usage_count[text_input]) >= 1:
            await message.reply_text(
                f"❌ سنوورێ ڤی کۆدی تەواو بوو (تنێ بۆ 1 کەسی بوو و کەسەکی دی بکار ئینایە).\n"
                f"💎 بۆ وەرگرتنا Free Key سەرەدانا خودانی بکە: {OWNER_USERNAME}\n"
                f"⏰ وقت بغداد: `{get_baghdad_time()}`"
            )
            return

        secret_code_usage_count[text_input].add(user_id)
        stats["claimed_secret_codes"].add(text_input)
        reward_val = ALL_SECRET_CODES[text_input]
        stats["balance"] += reward_val
        stats["xp"] += 5000
        
        await message.reply_text(
            f"🎉 **پیرۆزە! +{reward_val:,} Balance (کۆدێ ڤەشارتی یێ Omega) هاتە زێدەکرن!**\n"
            f"💰 Balance-ێ نوو: `{stats['balance']:,}` Key\n"
            f"⏰ وقت بغداد: `{get_baghdad_time()}`"
        )
        return

    if not text_input.startswith("http"):
        # Check if user has zero balance or low balance to suggest contacting owner
        free_key_text = ""
        if stats["balance"] < 1:
            free_key_text = f"\n\n💎 Balance-ێ تە نەما! بۆ وەرگرتنا Free Key سەرەدانا خودانی بکە: {OWNER_USERNAME}"
        
        await message.reply_text(
            f"⚠️ ژکەرەما خۆ لینکا دروست (YouTube, TikTok, Instagram) یان کۆدەکێ ڕاست بنێرە!{free_key_text}\n"
            f"⏰ وقت بغداد: `{get_baghdad_time()}`"
        )
        return

    if stats["balance"] < 1:
        await message.reply_text(
            f"❌ Balance-ێ تە نینە! (1 Key پێدڤییە بۆ داونلۆدکرنێ).\n"
            f"💎 بۆ وەرگرتنا Free Key سەرەدانا خودانی بکە: {OWNER_USERNAME}\n"
            f"⏰ وقت بغداد: `{get_baghdad_time()}`"
        )
        return

    stats["links_count"] += 1
    process_msg = await message.reply_text(f"⚡️ MX DOWNLOAD (Omega Engine - 720FPS) خەریکە زانیاریان ئینیت خوارێ...\n⏰ وقت بغداد: `{get_baghdad_time()}`")

    try:
        ydl_opts = {'quiet': True, 'format': 'best', 'extractor_args': {'youtube': {'player_client': ['android', 'web']}}}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text_input, download=False)
            title = info.get('title', 'MX Omega Media')

        action_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 MP4 (No Watermark - 1 Key)", callback_data=f"dl_mp4|{text_input}"), InlineKeyboardButton("🎵 MP3 (1 Key)", callback_data=f"dl_mp3_full|{text_input}")],
            [InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]
        ])
        await process_msg.edit_text(
            f"🎬 ناڤ: {title}\n"
            f"💰 Balance: `{stats['balance']}` Key (نرخ: 1 Key)\n"
            f"🚀 کواليتى: 720 FPS Hyper Quantum Smooth (No Watermark)\n\n"
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
    stats = user_stats.setdefault(user_id, {"balance": 0, "downloads_count": 0, "downloaded_videos": [], "xp": 0})
    
    if stats["balance"] < 1:
        await callback_query.answer(f"❌ Balance-ێ تە نینە! (1 Key پێدڤییە). بۆ Free Key سەرەدانا {OWNER_USERNAME} بکە.", show_alert=True)
        return

    stats["balance"] -= 1
    status_msg = await callback_query.message.reply_text(
        f"⏳ MX DOWNLOAD (720FPS Omega Engine) خەریکە دابەزینت (No Watermark)...\n"
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
                caption=f"🎬 MP4 (No Watermark - 720FPS Omega) هاتە داونلۆدکرن!\n💰 Balance: `{stats['balance']}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`"
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
                audio=filename, title=title, performer="MX Omega Supreme God",
                caption=f"🎶 MP3 هاتە داونلۆدکرن!\n💰 Balance: `{stats['balance']}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`"
            )

        stats["downloads_count"] += 1
        stats["xp"] += 25
        if stats["downloads_count"] >= 100:
            stats["level"] = "Omega Overlord God"
        elif stats["downloads_count"] >= 50:
            stats["level"] = "Supreme Master"
        elif stats["downloads_count"] >= 10:
            stats["level"] = "Omega Pro"

        global_total_downloads += 1
        stats["downloaded_videos"].append(title[:30])
        
        if filename and os.path.exists(filename):
            os.remove(filename)
        await status_msg.delete()
    except Exception as e:
        stats["balance"] += 1  # Refund 1 Key automatically on any error
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        await status_msg.edit_text(f"❌ هەڵە د دابەزاندنێ دا (1 Key هاتە ڤەگەراندن):\n`{str(e)}`\n⏰ وقت بغداد: `{get_baghdad_time()}`")

app.run()
