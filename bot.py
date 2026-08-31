import os
import asyncio
import time
import random
import string
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import UserNotParticipant
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")
REQUIRED_CHANNEL = "LEGEND_MODS33"

app = Client(
    "supreme_trillion_ultimate_v26_surchi_mx",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    sleep_threshold=0
)

user_stats = {}
global_total_downloads = 0
user_cooldown = {}
banned_users = set()
secret_code_usage_count = {}

LEGEND_75_SECRET_CODES = {
    "LEGEND-MX-9X8K2M1P4L0": 600, "LEGEND-MX-3T7W8Q2N5H9": 600, "LEGEND-MX-6Y1R4V8K3J2": 600,
    "LEGEND-MX-5F9P2M7T1X4": 600, "LEGEND-MX-8H3N6W9Q2L5": 600, "LEGEND-MX-1K4T7R3P6V8": 600,
    "LEGEND-MX-2J5Y8M1N4X7": 600, "LEGEND-MX-7Q9W2K5H8T1": 600, "LEGEND-MX-4P1R6V3L9N2": 600,
    "LEGEND-MX-9M2T5X8K1H4": 600, "LEGEND-MX-3V6N9Q2P5R7": 600, "LEGEND-MX-6K8W1T4J7Y3": 600,
    "LEGEND-MX-2P5M8V1X4N9": 600, "LEGEND-MX-7T3Q6K9R2H5": 600, "LEGEND-MX-1N4Y7W3P6L8": 600,
    "LEGEND-MX-5R8K2T5V1X9": 600, "LEGEND-MX-8X1N4M7Q3J6": 600, "LEGEND-MX-3W6P9R2H5T1": 600,
    "LEGEND-MX-6Y2T5K8L1N4": 600, "LEGEND-MX-9V4Q7W3P6R2": 600, "LEGEND-MX-2K8N1M4T7X5": 600,
    "LEGEND-MX-5P3R6V9H2L1": 600, "LEGEND-MX-8T1W4K7N3Y9": 600, "LEGEND-MX-1M6Q9P2X5R8": 600,
    "LEGEND-MX-4H2T5V8J1N3": 600, "LEGEND-MX-7X9N2K6R4H7": 600, "LEGEND-MX-3P1W5M8T2L6": 600,
    "LEGEND-MX-6R4V7Q1N9K3": 600, "LEGEND-MX-9K2T5X8P3J1": 600, "LEGEND-MX-2N7W1M4H6R5": 600,
    "LEGEND-MX-5V8P3Q6N1Y2": 600, "LEGEND-MX-8Y1K4T7R9X3": 600, "LEGEND-MX-1T6M9V2P5L4": 600,
    "LEGEND-MX-4N3R6K9H1T8": 600, "LEGEND-MX-7W2P5X8N3Q1": 600, "LEGEND-MX-3K9T2V6R1J5": 600,
    "LEGEND-MX-6M1W4N7P2Y8": 600, "LEGEND-MX-9P8R3K6T5X1": 600, "LEGEND-MX-2H5Q1M4V9N3": 600,
    "LEGEND-MX-5T7W2X6R8L1": 600, "LEGEND-MX-8N4K1P9T3J2": 600, "LEGEND-MX-1V6M3Q8H5Y7": 600,
    "LEGEND-MX-4R9T2N6X1P4": 600, "LEGEND-MX-7K1W5V8R3N2": 600, "LEGEND-MX-3P4M7Q1T6H9": 600,
    "LEGEND-MX-6X2N9K3P5L8": 600, "LEGEND-MX-9T5R1W4J7Y2": 600, "LEGEND-MX-2M8V3Q6N1X4": 600,
    "LEGEND-MX-5H1T4K7P9R3": 600, "LEGEND-MX-8W6N2M5X1L7": 600, "LEGEND-MX-1P9R4T7V3H2": 600,
    "LEGEND-MX-4K3Q6N1Y5J8": 600, "LEGEND-MX-7T2M5X8R1N9": 600, "LEGEND-MX-3V1W8P4K6T3": 600,
    "LEGEND-MX-6N7R2M9Q5H1": 600, "LEGEND-MX-9X4K1T6L3Y8": 600, "LEGEND-MX-2P8V5N1X7J4": 600,
    "LEGEND-MX-5M3T9Q2R6H1": 600, "LEGEND-MX-8K1W6P3N7V2": 600, "LEGEND-MX-1T4R7X2Y5L9": 600,
    "LEGEND-MX-4N9M3V6H1T8": 600, "LEGEND-MX-7W2K5P8Q3N1": 600, "LEGEND-MX-3X6T1R4J9Y5": 600,
    "LEGEND-MX-6P8N2M5V1X3": 600, "LEGEND-MX-9V1W7K3T6H2": 600, "LEGEND-MX-2R4Q9N1L5P8": 600,
    "LEGEND-MX-5T3M6X8R2J1": 600, "LEGEND-MX-8H1P4V7K9N3": 600, "LEGEND-MX-1N6W2T5Y3L4": 600,
    "LEGEND-MX-4K9R3Q6X1P7": 600, "LEGEND-MX-7M2T5N8H1V6": 600, "LEGEND-MX-3V8P1K4T9Y2": 600,
    "LEGEND-MX-6X4N7M2R5J1": 600, "LEGEND-MX-9T1W5Q8L3H4": 600, "LEGEND-MX-2P6K3V9N1X7": 600
}

for code in LEGEND_75_SECRET_CODES:
    secret_code_usage_count[code] = set()

async def check_user_channel_membership(client, user_id):
    try:
        member = await client.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
    except UserNotParticipant:
        return False
    except Exception:
        pass
    return False

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 پروفایلا پێشکەفتى", callback_data="my_profile"),
            InlineKeyboardButton("📥 ڤیدیۆیێن داونلۆدكري", callback_data="my_downloads")
        ],
        [
            InlineKeyboardButton("📥 Mx Video Download", callback_data="mx_video_download_menu"),
            InlineKeyboardButton("🎁 خەلاتێن 3 ساعتی (10 Key)", callback_data="legend_mx_claim")
        ],
        [
            InlineKeyboardButton("🎁 خەلاتێن ڕۆژانە (کۆدێ 75 Key)", callback_data="daily_bonus")
        ],
        [
            InlineKeyboardButton("📊 ئامارێن گشتی یێن بۆتی", callback_data="bot_global_stats"),
            InlineKeyboardButton("💡 رێنمایێن بەکارهۆنانێ", callback_data="bot_help")
        ],
        [
            InlineKeyboardButton("⚙️ سیستەم و پشکنین", callback_data="system_status"),
            InlineKeyboardButton("👑 خودان و دامەزرێنەر: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
        ]
    ])

@app.on_message(filters.command("start"))
async def start_command_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.reply_text("❌ لێبوورین، تو هاتیە بلۆککرن.")
        return

    is_member = await check_user_channel_membership(client, user_id)
    if not is_member:
        join_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 پشکداربوون د چەنەلێ دا", url="https://t.me/LEGEND_MODS33")],
            [InlineKeyboardButton("🔄 پشکنینا پشکداریێ (Check)", callback_data="check_membership")]
        ])
        await message.reply_text(
            "⚠️ بۆ کارئینانا ڤی بۆتی، دڤێت پێش هەمی تشتن پشکدار بی د چەنەلا مە دا:\n\n"
            "🔗 https://t.me/LEGEND_MODS33\n\n"
            "پشتی پشکداربوونێ، دوگمەیا پشکنینێ کلیک بکە! 👇",
            reply_markup=join_kb
        )
        return

    user_name = message.from_user.first_name or "User"
    user_username = f"@{message.from_user.username}" if message.from_user.username else "نەدیار"

    if user_id not in user_stats:
        unique_daily_code = f"MX-DAY-{user_id}-{random.randint(1000, 9999)}"
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0,
            "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو",
            "last_links": [], "bonus_claimed": False, "balance": 0,
            "last_claim_time": 0, "last_daily_time": 0, "legend_mx_active": False,
            "daily_code": unique_daily_code, "claimed_secret_codes": set()
        }

    current_bal = user_stats[user_id]['balance']
    current_code = user_stats[user_id]['daily_code']

    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی یا هێزدارترین سیستەمێ داونلۆدکرنێ یێ جیهانێ!\n\n"
        f"💰 Balance-ێ تە یێ نها: `{current_bal}` Key\n"
        f"🎁 کۆدێ ڕۆژانەیێ تە (75 Key): `{current_code}`\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دابەزاندنێ، تنێ لینکێ خۆ ل ڤێرە بنێرە!"
    )
    await message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^check_membership"))
async def check_membership_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    is_member = await check_user_channel_membership(client, user_id)
    if not is_member:
        await callback_query.answer("❌ تو هێشتا پشکدار نینەی د چەنەلێ دا!", show_alert=True)
        return

    await callback_query.answer("✅ پشکداری هاتە پەسەندکرن!", show_alert=True)
    user_name = callback_query.from_user.first_name or "User"
    user_username = f"@{callback_query.from_user.username}" if callback_query.from_user.username else "نەدیار"

    if user_id not in user_stats:
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0,
            "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو",
            "last_links": [], "bonus_claimed": False, "balance": 0, "last_claim_time": 0,
            "legend_mx_active": False, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}",
            "last_daily_time": 0, "claimed_secret_codes": set()
        }

    current_bal = user_stats[user_id]['balance']
    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی!\n\n"
        f"💰 Balance-ێ تە: `{current_bal}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    await callback_query.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^mx_video_download_menu"))
async def mx_video_download_menu_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_stats.setdefault(user_id, {"balance": 0})
    bal = user_stats[user_id]["balance"]
    menu_text = (
        "📥 **Mx Video Download Lab:**\n\n"
        f"💰 Balance-ێ تە: `{bal}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(menu_text, reply_markup=kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^legend_mx_claim"))
async def legend_mx_claim_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if not await check_user_channel_membership(client, user_id):
        await callback_query.answer("❌ بۆ وەرگرتنا خەلاتی، دڤێت پشکدار بی د چەنەلا مە دا!", show_alert=True)
        return

    current_t = time.time()
    stats = user_stats.setdefault(user_id, {"balance": 0, "last_claim_time": 0, "downloads_count": 0, "success_count": 0, "links_count": 0, "rank": "⭐ ئەندامێ نوو", "last_links": [], "bonus_claimed": False, "legend_mx_active": False, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0, "claimed_secret_codes": set()})
    
    if current_t - stats["last_claim_time"] < 10800:
        remaining = int(10800 - (current_t - stats["last_claim_time"]))
        await callback_query.answer(f"⏳ چاڤەڕێی {remaining // 3600} دەمژمێران بن.", show_alert=True)
        return
        
    stats["last_claim_time"] = current_t
    stats["balance"] += 10
    await callback_query.message.edit_text(
        f"🎁 **پیرۆزە! +10 Key هاتە زێدەکرن!**\n💰 Balance: `{stats['balance']}` Key\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]])
    )
    await callback_query.answer("🎉 10 Key هاتنە وەرگرتن!")

@app.on_callback_query(filters.regex(r"^my_profile"))
async def profile_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.setdefault(user_id, {"balance": 0, "links_count": 0, "downloads_count": 0, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}"})
    profile_text = (
        f"👤 **پروفایلا تە:**\n\n"
        f"🔹 ناڤ: `{callback_query.from_user.first_name}`\n"
        f"• 💰 Balance: `{stats['balance']}` Key\n"
        f"• 🎁 کۆدێ ڕۆژانە (75 Key): `{stats['daily_code']}`\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 نووکرن (Refresh)", callback_data="my_profile"), InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]
    ])
    await callback_query.message.edit_text(profile_text, reply_markup=kb)
    await callback_query.answer("🔄 نوو بوو!")

@app.on_callback_query(filters.regex(r"^my_downloads"))
async def downloads_callback_handler(client, callback_query: CallbackQuery):
    stats = user_stats.get(callback_query.from_user.id, {"downloads_count": 0, "balance": 0})
    await callback_query.message.edit_text(
        f"📥 **داونلۆدێن تە:** {stats['downloads_count']}\n💰 Balance: `{stats['balance']}` Key\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]])
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_global_stats"))
async def global_stats_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    await callback_query.message.edit_text(
        f"📊 **ئامارێن گشتی:**\n👥 کاربەر: `{len(user_stats)}`\n📥 گشتی داونلۆد: `{global_total_downloads}`\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]])
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_help"))
async def bot_help_handler(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "💡 **رێنمایێن بەکارهۆنانێ:**\n• 75 کۆدێن ڤەشارتى هەنە (600 Key بۆ هەر ئێکێ و تنێ 2 کەس).\n• نرخێ داونلۆدکرنێ 2 Key یە.\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]])
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^system_status"))
async def system_status_handler(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "⚙️ **سیستەم ب ڕێکوپێکی کار دکەت.**\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]])
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^daily_bonus"))
async def daily_bonus_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if not await check_user_channel_membership(client, user_id):
        await callback_query.answer("❌ بۆ وەرگرتنێ پشکدار بی د چەنەلێ دا!", show_alert=True)
        return

    stats = user_stats.setdefault(user_id, {"balance": 0, "last_daily_time": 0, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}" , "claimed_secret_codes": set()})
    if time.time() - stats["last_daily_time"] < 86400:
        await callback_query.answer("⏳ تنێ جارەکێ د 24 دەمژمێران دا!", show_alert=True)
        return

    stats["last_daily_time"] = time.time()
    stats["balance"] += 75
    await callback_query.message.edit_text(
        f"🎁 **+75 Key هاتە زێدەکرن!**\n💰 Balance: `{stats['balance']}` Key\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]])
    )
    await callback_query.answer("🎉 پیرۆزە!")

@app.on_callback_query(filters.regex(r"^back_home"))
async def back_home_handler(client, callback_query: CallbackQuery):
    bal = user_stats.setdefault(callback_query.from_user.id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🌟 سڵاو!\n💰 Balance-ێ تە: `{bal}` Key\n\n👑 خودان: @YUSEEF_SURCHI",
        reply_markup=get_main_menu_keyboard()
    )
    await callback_query.answer()

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def downloader_core_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        return

    if not await check_user_channel_membership(client, user_id):
        join_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 پشکداربوون", url="https://t.me/LEGEND_MODS33")],
            [InlineKeyboardButton("🔄 پشکنین", callback_data="check_membership")]
        ])
        await message.reply_text("⚠️ دڤێت پشکدار بی د چەنەلا مە دا!", reply_markup=join_kb)
        return

    text_input = message.text.strip()
    stats = user_stats.setdefault(user_id, {"balance": 0, "links_count": 0, "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو", "last_links": [], "bonus_claimed": False, "last_claim_time": 0, "legend_mx_active": False, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0, "claimed_secret_codes": set()})

    if text_input in LEGEND_75_SECRET_CODES:
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
            f"🎉 **پیرۆزە! +600 Balance هاتە زێدەکرن!**\n💰 Balance-ێ نوو: `{stats['balance']}` Key\n\n👑 خودان: @YUSEEF_SURCHI"
        )
        return

    if text_input == stats["daily_code"]:
        if time.time() - stats["last_daily_time"] < 86400:
            await message.reply_text("⏳ تنێ جارەکێ د 24 دەمژمێران دا!")
            return
        stats["last_daily_time"] = time.time()
        stats["balance"] += 75
        await message.reply_text(
            f"🎁 **+75 Key هاتە زێدەکرن!**\n💰 Balance-ێ نوو: `{stats['balance']}` Key\n\n👑 خودان: @YUSEEF_SURCHI"
        )
        return

    if not text_input.startswith("http"):
        await message.reply_text("⚠️ لینک یان کۆدێ نەدروست!\n\n👑 خودان: @YUSEEF_SURCHI")
        return

    stats["links_count"] += 1
    process_msg = await message.reply_text("⚡️ زانیاری دئینم خوارێ...\n\n👑 خودان: @YUSEEF_SURCHI")

    try:
        ydl_opts = {'quiet': True, 'format': 'best', 'extractor_args': {'youtube': {'player_client': ['android', 'web']}}}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text_input, download=False)
            title = info.get('title', 'Media')

        action_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 MP4 (2 Key)", callback_data=f"dl_mp4|{text_input}"), InlineKeyboardButton("🎵 MP3 (2 Key)", callback_data=f"dl_mp3_full|{text_input}")],
            [InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")]
        ])
        await process_msg.edit_text(f"🎬 ناڤ: {title}\n💰 Balance: `{stats['balance']}` Key\n\nکوالیتیا خۆ هەڵبژێرە 👇\n\n👑 خودان: @YUSEEF_SURCHI", reply_markup=action_kb)
    except Exception as e:
        await process_msg.edit_text(f"❌ هەڵە: `{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI")

@app.on_callback_query(filters.regex(r"^dl_"))
async def download_callback_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    user_id = callback_query.from_user.id
    if not await check_user_channel_membership(client, user_id):
        await callback_query.answer("❌ دڤێت پشکدار بی د چەنەلێ دا!", show_alert=True)
        return

    action, url_link = callback_query.data.split("|", 1)
    stats = user_stats.setdefault(user_id, {"balance": 0, "downloads_count": 0})
    
    if stats["balance"] < 2:
        await callback_query.answer("❌ Balance-ێ تە کێمە! پێدڤییە حداقل 2 Key هەبت.", show_alert=True)
        return

    stats["balance"] -= 2
    status_msg = await callback_query.message.reply_text(f"⏳ خەریکە دابەزینم... (Balance: {stats['balance']})\n\n👑 خودان: @YUSEEF_SURCHI")
    
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
            await callback_query.message.reply_video(video=filename, caption=f"🎬 MP4 هاتە داونلۆدکرن!\n💰 Balance: {stats['balance']}\n\n👑 خودان: @YUSEEF_SURCHI")
        else:
            ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'downloads/%(id)s.%(ext)s', 'quiet': True, 'extractor_args': {'youtube': {'player_client': ['android', 'web']}}}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_link, download=True)
                filename = ydl.prepare_filename(info)
            await callback_query.message.reply_audio(audio=filename, title=info.get('title', 'Audio'), performer="YUSEEF_SURCHI", caption=f"🎶 MP3 هاتە داونلۆدکرن!\n💰 Balance: {stats['balance']}\n\n👑 خودان: @YUSEEF_SURCHI")

        stats["downloads_count"] += 1
        global_total_downloads += 1
        if filename and os.path.exists(filename):
            os.remove(filename)
        await status_msg.delete()
    except Exception as e:
        stats["balance"] += 2
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        await status_msg.edit_text(f"❌ هەڵە، Key هاتە ڤەگەراندن:\n`{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI")

app.run()
