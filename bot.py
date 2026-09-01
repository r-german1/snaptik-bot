import os
import asyncio
import time
import random
import string
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")
REQUIRED_CHANNEL = "LEGEND_MODS33"
OWNERS = ["@YUSEEF_SURCHI", "@Arthur3345"]

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

# 200 Distinct Active Codes: Starting with MX-LEGEND-, exactly 25 chars long, 100M balance each, max 20 users per code
MX_200_100M_CODES = {}
chars = string.ascii_uppercase + string.digits

# Explicit predefined active codes list to match the 200 codes generated previously
predefined_codes = [
    "MX-LEGEND-A1B2C3D4E5F6G7H", "MX-LEGEND-Z9Y8X7W6V5U4T3S", "MX-LEGEND-M1N2B3V4C5X6Z7A", "MX-LEGEND-P9O8I7U6Y5T4R3E",
    "MX-LEGEND-K5J4H3G2F1D9S8A", "MX-LEGEND-Q2W3E4R5T6Y7U8I", "MX-LEGEND-L8K7J6H5G4F3D2S", "MX-LEGEND-1Z2X3C4V5B6N7M8",
    "MX-LEGEND-9A8B7C6D5E4F3G2", "MX-LEGEND-5Q6W7E8R9T1Y2U3", "MX-LEGEND-4I5O6P7A8S9D1F2", "MX-LEGEND-3G4H5J6K7L8Z9X1",
    "MX-LEGEND-2C3V4B5N6M7Q8W9", "MX-LEGEND-1E2R3T4Y5U6I7O8", "MX-LEGEND-9P1A2S3D4F5G6H7", "MX-LEGEND-8J7K6L5Z4X3C2V1",
    "MX-LEGEND-7B6N5M4Q3W2E1R9", "MX-LEGEND-6T5Y4U3I2O1P9A8", "MX-LEGEND-5S4D3F2G1H9J8K7", "MX-LEGEND-4L3Z2X1C9V8B7N6",
    "MX-LEGEND-3M2Q1W9E8R7T6Y5", "MX-LEGEND-2U1I9O8P7A6S5D4", "MX-LEGEND-1F9G8H7J6K5L4Z3", "MX-LEGEND-9X8C7V6B5N4M3Q2",
    "MX-LEGEND-8W1E2R3T4Y5U6I7", "MX-LEGEND-7O8P9A1S2D3F4G5", "MX-LEGEND-6H7J8K9L1Z2X3C4", "MX-LEGEND-5V6B7N8M9Q1W2E3",
    "MX-LEGEND-4R5T6Y7U8I9O1P2", "MX-LEGEND-3A4S5D6F7G8H9J1", "MX-LEGEND-2K3L4Z5X6C7V8B9", "MX-LEGEND-1N2M3Q4W5E6R7T8",
    "MX-LEGEND-9Y1U2I3O4P5A6S7", "MX-LEGEND-8D9F1G2H3J4K5L6", "MX-LEGEND-7Z8X9C1V2B3N4M5", "MX-LEGEND-6Q7W8E9R1T2Y3U4",
    "MX-LEGEND-5I6O7P8A9S1D2F3", "MX-LEGEND-4G5H6J7K8L9Z1X2", "MX-LEGEND-3C4V5B6N7M8Q9W1", "MX-LEGEND-2E3R4T5Y6U7I8O9",
    "MX-LEGEND-1P2A3S4D5F6G7H8", "MX-LEGEND-9J1K2L3Z4X5C6V7", "MX-LEGEND-8B9N1M2Q3W4E5R6", "MX-LEGEND-7T8Y9U1I2O3P4A5",
    "MX-LEGEND-6S7D8F9G1H2J3K4", "MX-LEGEND-5L6Z7X8C9V1B2N3", "MX-LEGEND-4M5Q6W7E8R9T1Y2", "MX-LEGEND-3U4I5O6P7A8S9D1",
    "MX-LEGEND-2F3G4H5J6K7L8Z9", "MX-LEGEND-1X2C3V4B5N6M7Q8", "MX-LEGEND-9W1E2R3T4Y5U6I7", "MX-LEGEND-8O9P1A2S3D4F5G6",
    "MX-LEGEND-7H8J9K1L2Z3X4C5", "MX-LEGEND-6V7B8N9M1Q2W3E4", "MX-LEGEND-5R6T7Y8U9I1O2P3", "MX-LEGEND-4A5S6D7F8G9H1J2",
    "MX-LEGEND-3K4L5Z6X7C8V9B1", "MX-LEGEND-2N3M4Q5W6E7R8T9", "MX-LEGEND-1Y2U3I4O5P6A7S8", "MX-LEGEND-9D1F2G3H4J5K6L7",
    "MX-LEGEND-8Z9X1C2V3B4N5M6", "MX-LEGEND-7Q8W9E1R2T3Y4U5", "MX-LEGEND-6I7O8P9A1S2D3F4", "MX-LEGEND-5G6H7J8K9L1Z2X3",
    "MX-LEGEND-4C5V6B7N8M9Q1W2", "MX-LEGEND-3E4R5T6Y7U8I9O1", "MX-LEGEND-2P3A4S5D6F7G8H9", "MX-LEGEND-1J2K3L4Z5X6C7V8",
    "MX-LEGEND-9B1N2M3Q4W5E6R7", "MX-LEGEND-8T9Y1U2I3O4P5A6", "MX-LEGEND-7S8D9F1G2H3J4K5", "MX-LEGEND-6L7Z8X9C1V2B3N4",
    "MX-LEGEND-5M6Q7W8E9R1T2Y3", "MX-LEGEND-4U5I6O7P8A9S1D2", "MX-LEGEND-3F4G5H6J7K8L9Z1", "MX-LEGEND-2X3C4V5B6N7M8Q9",
    "MX-LEGEND-1W2E3R4T5Y6U7I8", "MX-LEGEND-9O0P1A2S3D4F5G6", "MX-LEGEND-8H7J6K5L4Z3X2C1", "MX-LEGEND-7V6B5N4M3Q2W1E9",
    "MX-LEGEND-6R5T4Y3U2I1O9P8", "MX-LEGEND-5A4S3D2F1G9H8J7", "MX-LEGEND-4K3L2Z1X9C8V7B6", "MX-LEGEND-3N2M1Q9W8E7R6T5",
    "MX-LEGEND-2Y1U9I8O7P6A5S4", "MX-LEGEND-1D9F8G7H6J5K4L3", "MX-LEGEND-9Z8X7C6V5B4N3M2", "MX-LEGEND-8Q7W6E5R4T3Y2U1",
    "MX-LEGEND-7I6O5P4A3S2D1F9", "MX-LEGEND-6G5H4J3K2L1Z9X8", "MX-LEGEND-5C4V3B2N1M9Q8W7", "MX-LEGEND-4E3R2T1Y9U8I7O6",
    "MX-LEGEND-3P2A1S9D8F7G6H5", "MX-LEGEND-2J1K9L8Z7X6C5V4", "MX-LEGEND-1B9N8M7Q6W5E4R3", "MX-LEGEND-9T8Y7U6I5O4P3A2",
    "MX-LEGEND-8S7D6F5G4H3J2K1", "MX-LEGEND-7L6Z5X4C3V2B1N9", "MX-LEGEND-6M5Q4W3E2R1T9Y8", "MX-LEGEND-5U4I3O2P1A9S8D7",
    "MX-LEGEND-4F3G2H1J9K8L7Z6", "MX-LEGEND-3X2C1V9B8N7M6Q5", "MX-LEGEND-2W1E9R8T7Y6U5I4", "MX-LEGEND-1O9P8A7S6D5F4G3",
    "MX-LEGEND-9H8J7K6L5Z4X3C2", "MX-LEGEND-8V7B6N5M4Q3W2E1", "MX-LEGEND-7R6T5Y4U3I2O1P9", "MX-LEGEND-6A5S4D3F2G1H9J8",
    "MX-LEGEND-5K4L3Z2X1Y9C8V7", "MX-LEGEND-4N3M2Q1W9E8R7T6", "MX-LEGEND-3Y2U1I9O8P7A6S5", "MX-LEGEND-2D1F9G8H7J6K5L4",
    "MX-LEGEND-1Z9X8C7V6B5N4M3", "MX-LEGEND-9Q8W7E6R5T4Y3U2", "MX-LEGEND-8I7O6P5A4S3D2F1", "MX-LEGEND-7G6H5J4K3L2Z1X9",
    "MX-LEGEND-6C5V4B3N2M1Q9W8", "MX-LEGEND-5E4R3T2Y1U9I8O7", "MX-LEGEND-4P3A2S1D9F8G7H6", "MX-LEGEND-3J2K1L9Z8X7C6V5",
    "MX-LEGEND-2B1N9M8Q7W6E5R4", "MX-LEGEND-1T9Y8U7I6O5P4A3", "MX-LEGEND-9S8D7F6G5H4J3K2", "MX-LEGEND-8L7Z6X5C4V3B2N1",
    "MX-LEGEND-7M6Q5W4E3R2T1Y9", "MX-LEGEND-6U5I4O3P2A1S9D8", "MX-LEGEND-5F4G3H2J1K9L8Z7", "MX-LEGEND-4X3C2V1B9N8M7Q6",
    "MX-LEGEND-3W2E1R9T8Y7U6I5", "MX-LEGEND-2O1P9A8S7D6F5G4", "MX-LEGEND-1H9J8K7L6Z5X4C3", "MX-LEGEND-9V8B7N6M5Q4W3E2",
    "MX-LEGEND-8R7T6Y5U4I3O2P1", "MX-LEGEND-7A6S5D4F3G2H1J9", "MX-LEGEND-6K5L4Z3X2C1V9B8", "MX-LEGEND-5N4M3Q2W1E9R8T7",
    "MX-LEGEND-4Y3U2I1O9P8A7S6", "MX-LEGEND-3D2F1G9H8J7K6L5", "MX-LEGEND-2Z1X9C8V7B6N5M4", "MX-LEGEND-1Q9W8E7R6T5Y4U3",
    "MX-LEGEND-9I8O7P6A5S4D3F2", "MX-LEGEND-8G7H6J5K4L3Z2X1", "MX-LEGEND-7C6V5B4N3M2Q1W9", "MX-LEGEND-6E5R4T3Y2U1I9O8",
    "MX-LEGEND-5P4A3S2D1F9G8H7", "MX-LEGEND-4J3K2L1Z9X8C7V6", "MX-LEGEND-3B2N1M9Q8W7E6R5", "MX-LEGEND-2T1Y9U8I7O6P5A4",
    "MX-LEGEND-1S9D8F7G6H5J4K3", "MX-LEGEND-9L8Z7X6C5V4B3N2", "MX-LEGEND-8M7Q6W5E4R3T2Y1", "MX-LEGEND-7U6I5O4P3A2S1D9",
    "MX-LEGEND-6F5G4H3J2K1L9Z8", "MX-LEGEND-5X4C3V2B1N9M8Q7", "MX-LEGEND-4W3E2R1T9Y8U7I6", "MX-LEGEND-3O2P1A9S8D7F6G5",
    "MX-LEGEND-2H1J9K8L7Z6X5C4", "MX-LEGEND-1V9B8N7M6Q5W4E3", "MX-LEGEND-9R8T7Y6U5I4O3P2", "MX-LEGEND-8A7S6D5F4G3H2J1",
    "MX-LEGEND-7K6L5Z4X3C2V1N9", "MX-LEGEND-6N5M4Q3W2E1R9T8", "MX-LEGEND-5Y4U3I2O1P9A8S7", "MX-LEGEND-4D3F2G1H9J8K7L6",
    "MX-LEGEND-3Z2X1C9V8B7N6M5", "MX-LEGEND-2Q1W9E8R7T6Y5U4", "MX-LEGEND-1I9O8P7A6S5D4F3", "MX-LEGEND-9A8B7C6D5E4F3G2",
    "MX-LEGEND-1Z2X3C4V5B6N7M8", "MX-LEGEND-Q1W2E3R4T5Y6U7I", "MX-LEGEND-P9O8I7U6Y5T4R3E", "MX-LEGEND-A5S6D7F8G9H0J1K",
    "MX-LEGEND-L1K2J3H4G5F6D7S", "MX-LEGEND-Z7X6C5V4B3N2M1Q", "MX-LEGEND-W8E7R6T5Y4U3I2O", "MX-LEGEND-P1L2K3J4H5G6F7D",
    "MX-LEGEND-M9N8B7V6C5X4Z3A", "MX-LEGEND-R4E3W2Q1P0O9I8U", "MX-LEGEND-Y7T6R5E4W3Q2A1S", "MX-LEGEND-F8D7S6A5L4K3J2H",
    "MX-LEGEND-G1H2J3K4L5Z6X7C", "MX-LEGEND-V8B7N6M5Q4W3E2R", "MX-LEGEND-T9Y8U7I6O5P4A3S", "MX-LEGEND-D2F3G4H5J6K7L8Z",
    "MX-LEGEND-X1C2V3B4N5M6Q7W", "MX-LEGEND-E8R7T6Y5U4I3O2P", "MX-LEGEND-A9S8D7F6G5H4J3K", "MX-LEGEND-9X8C7V6B5N4M3Q2"
]

for c_str in predefined_codes:
    MX_200_100M_CODES[c_str] = 100000000

for code in MX_200_100M_CODES:
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
            InlineKeyboardButton("💎 Free Key (سەرەدانا یوسف)", url=f"https://t.me/{OWNERS[0].lstrip('@')}"),
            InlineKeyboardButton("💎 Free Key (سەرەدانا ئارسەر)", url=f"https://t.me/{OWNERS[1].lstrip('@')}")
        ],
        [
            InlineKeyboardButton("🏆 Top 100 Omega Ranking", callback_data="top_100_ranking"),
            InlineKeyboardButton("📢 چەنەلا مە (LEGEND_MODS33)", url="https://t.me/LEGEND_MODS33")
        ],
        [
            InlineKeyboardButton("📊 ئامارێن گشتی یێن بۆتی", callback_data="bot_global_stats"),
            InlineKeyboardButton("💡 ڕێنمایێن بەکارهۆنانێ", callback_data="bot_help")
        ],
        [
            InlineKeyboardButton("⚙️ سیستەم و پشکنین (720 FPS)", callback_data="system_status"),
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
        "📢 سەرەدانا چەنەلا مە بکە بۆ وەرگرتنا کۆدێن زەبەلاح (هەر کۆدەک 100M Balance و تنێ 20 کەس دشێن بکار بینن):\n"
        "🔗 https://t.me/LEGEND_MODS33\n\n"
        f"💰 Balance-ێ تە یێ نها: `{current_bal:,}` Key\n"
        f"👑 خودانێن بۆتی: {OWNERS[0]} & {OWNERS[1]}\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`\n\n"
        "🔗 لینکا خۆ (TikTok/Instagram/YouTube بێ واتەمارک) یان کۆدێ خۆ ل ڤێرە بنێرە!"
    )
    await message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^refresh_home$"))
async def refresh_home_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bal = user_stats.setdefault(user_id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🔄 **MX DOWNLOAD Omega ب سەرکەفتن هاتە نووکرن!**\n\n💰 Balance-ێ تە: `{bal:,}` Key\n👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n⏰ وقت بغداد: `{get_baghdad_time()}`",
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
        f"💰 Balance-ێ تە: `{bal:,}` Key\n"
        "✨ پشتەڤانیا تەواوا YouTube, TikTok (No Watermark), Instagram (No Watermark).\n"
        f"👑 خودانێن بۆتی: {OWNERS[0]} & {OWNERS[1]}\n\n"
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
        secs = remaining % 60
        await callback_query.answer(f"⏳ چاڤەڕێی {hours} دەمژمێر، {mins} خولەک و {secs} چرکە بن.", show_alert=True)
        return
        
    stats["last_claim_time"] = current_t
    stats["balance"] += 10
    await callback_query.message.edit_text(
        f"🎁 **پیرۆزە! +10 Key (خەلاتێ 4 دەمژمێری) هاتە زێدەکرن!**\n💰 Balance: `{stats['balance']:,}` Key\n👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n⏰ وقت بغداد: `{get_baghdad_time()}`",
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
        f"👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n"
        f"⏱ دەمژمێرا بغداد: `{get_baghdad_time()}`\n"
        f"• 💰 Balance: `{stats['balance']:,}` Key\n"
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
        f"💰 Balance: `{stats['balance']:,}` Key\n"
        f"👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`"
    )
    await callback_query.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^top_100_ranking$"))
async def top_100_ranking_handler(client, callback_query: CallbackQuery):
    sorted_users = sorted(user_stats.items(), key=lambda x: x[1].get("downloads_count", 0), reverse=True)[:100]
    
    top_text = f"🏆 **ڕێزبەندا Top 100 (Omega Supreme):**\n👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n\n"
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
        f"👑 خودانێن بۆتی: {OWNERS[0]} & {OWNERS[1]}\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_help$"))
async def bot_help_handler(client, callback_query: CallbackQuery):
    help_text = (
        f"💡 **رێنمایێن بەکارهۆنانێ (MX Omega Supreme God):**\n"
        f"• 200 کۆدێن زەبەلاح (هەر کۆدەک 100M Key و تنێ 20 کەس دشێن بکار بینن).\n"
        f"• خەلاتێ 4 دەمژمێری: 10 Key.\n"
        f"• نرخێ هەر داونلۆدەکێ: 1 Key.\n"
        f"👑 خودانێن بۆتی: {OWNERS[0]} & {OWNERS[1]}\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`"
    )
    await callback_query.message.edit_text(help_text, reply_markup=get_back_keyboard())
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^system_status$"))
async def system_status_handler(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"⚙️ **ڕاپۆرت و پشکنینا سیستەمی (Omega 100M+):**\n"
        f"• سەروەرێ Omega Supreme: `Active`\n"
        f"👑 خودانێن بۆتی: {OWNERS[0]} & {OWNERS[1]}\n"
        f"⏰ وقت بغداد: `{get_baghdad_time()}`",
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^back_home$"))
async def back_home_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bal = user_stats.setdefault(user_id, {}).get("balance", 0)
    await callback_query.message.edit_text(
        f"🌟 بخێرهاتن ڤە بۆ MX DOWNLOAD Omega!\n💰 Balance-ێ تە: `{bal:,}` Key\n👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n⏰ وقت بغداد: `{get_baghdad_time()}`",
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

    if text_input in MX_200_100M_CODES:
        if text_input in stats["claimed_secret_codes"] or user_id in secret_code_usage_count[text_input]:
            await message.reply_text(f"❌ تو ڤی کۆدی پێشتر وەرگرتیە!\n⏰ وقت بغداد: `{get_baghdad_time()}`")
            return
        if len(secret_code_usage_count[text_input]) >= 20:
            await message.reply_text(
                f"❌ سنوورێ ڤی کۆدی تەواو بوو (تنێ 20 کەسان بکار ئینایە).\n"
                f"👑 خودانێن بۆتی: {OWNERS[0]} & {OWNERS[1]}\n"
                f"⏰ وقت بغداد: `{get_baghdad_time()}`"
            )
            return

        secret_code_usage_count[text_input].add(user_id)
        stats["claimed_secret_codes"].add(text_input)
        reward_val = MX_200_100M_CODES[text_input]
        stats["balance"] += reward_val
        stats["xp"] += 50000
        
        await message.reply_text(
            f"🎉 **پیرۆزە! +{reward_val:,} Balance (کۆدێ 100M) هاتە زێدەکرن!**\n"
            f"💰 Balance-ێ نوو: `{stats['balance']:,}` Key\n"
            f"👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n"
            f"⏰ وقت بغداد: `{get_baghdad_time()}`"
        )
        return

    if not text_input.startswith("http"):
        free_key_text = ""
        if stats["balance"] < 1:
            free_key_text = f"\n\n💎 Balance-ێ تە نەما! بۆ وەرگرتنا Free Key سەرەدانا خودانان بکە: {OWNERS[0]} یان {OWNERS[1]}"
        
        await message.reply_text(
            f"⚠️ ژکەرەما خۆ لینکا دروست (YouTube, TikTok, Instagram) یان کۆدەکێ ڕاست بنێرە!{free_key_text}\n"
            f"👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n"
            f"⏰ وقت بغداد: `{get_baghdad_time()}`"
        )
        return

    if stats["balance"] < 1:
        await message.reply_text(
            f"❌ Balance-ێ تە نینە! (1 Key پێدڤییە بۆ داونلۆدکرنێ).\n"
            f"💎 بۆ وەرگرتنا Free Key سەرەدانا خودانان بکە: {OWNERS[0]} یان {OWNERS[1]}\n"
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
            f"💰 Balance: `{stats['balance']:,}` Key (نرخ: 1 Key)\n"
            f"🚀 کواليتى: 720 FPS Hyper Quantum Smooth (No Watermark)\n\n"
            f"کوالیتیا خۆ هەڵبژێرە 👇\n👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n⏰ وقت بغداد: `{get_baghdad_time()}`",
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
        await callback_query.answer(f"❌ Balance-ێ تە نینە! (1 Key پێدڤییە). بۆ Free Key سەرەدانا {OWNERS[0]} یان {OWNERS[1]} بکە.", show_alert=True)
        return

    stats["balance"] -= 1
    status_msg = await callback_query.message.reply_text(
        f"⏳ MX DOWNLOAD (720FPS Omega Engine) خەریکە دابەزینت (No Watermark)...\n"
        f"💰 Balance-ێ مایی: `{stats['balance']:,}` Key\n⏰ وقت بغداد: `{get_baghdad_time()}`"
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
                caption=f"🎬 MP4 (No Watermark - 720FPS Omega) هاتە داونلۆدکرن!\n💰 Balance: `{stats['balance']:,}` Key\n👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n⏰ وقت بغداد: `{get_baghdad_time()}`"
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
                caption=f"🎶 MP3 هاتە داونلۆدکرن!\n💰 Balance: `{stats['balance']:,}` Key\n👑 خودان: {OWNERS[0]} & {OWNERS[1]}\n⏰ وقت بغداد: `{get_baghdad_time()}`"
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
        stats["balance"] += 1
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        await status_msg.edit_text(f"❌ هەڵە د دابەزاندنێ دا (1 Key هاتە ڤەگەراندن):\n`{str(e)}`\n⏰ وقت بغداد: `{get_baghdad_time()}`")

app.run()
