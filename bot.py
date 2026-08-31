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
REQUIRED_CHANNEL = "LEGEND_MODS33"  # ناڤێ چەنەلا مەرجدار بۆ پشکداریێ

app = Client(
    "supreme_trillion_ultimate_v25_surchi_mx",
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

def generate_75_hidden_codes():
    codes = {}
    for _ in range(75):
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))
        code = f"LEGEND-MX-{random_suffix}"
        codes[code] = 600
        secret_code_usage_count[code] = set()
    return codes

LEGEND_75_SECRET_CODES = generate_75_hidden_codes()

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
        await message.reply_text("❌ لێبوورین، تو هاتیە بلۆککرن ژ کارئینانا ڤی بۆتی.")
        return

    is_member = await check_user_channel_membership(client, user_id)
    if not is_member:
        join_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 پشکداربوون د چەنەلێ دا", url="https://t.me/LEGEND_MODS33")],
            [InlineKeyboardButton("🔄 پشکنینا پشکداریێ (Check)", callback_data="check_membership")]
        ])
        await message.reply_text(
            "⚠️ **بۆ کارئینانا ڤی بۆتی، دڤێت پێش هەمی تشتن پشکدار بی د چەنەما مە دا:**\n\n"
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
            "name": user_name,
            "username": user_username,
            "links_count": 0,
            "downloads_count": 0,
            "success_count": 0,
            "rank": "⭐ ئەندامێ نوو",
            "last_links": [],
            "bonus_claimed": False,
            "balance": 0,  # دەستپێکرنا ب 0 Key
            "last_claim_time": 0,
            "last_daily_time": 0,
            "legend_mx_active": False,
            "daily_code": unique_daily_code,
            "claimed_secret_codes": set()
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
        unique_daily_code = f"MX-DAY-{user_id}-{random.randint(1000, 9999)}"
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0,
            "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو", 
            "last_links": [], "bonus_claimed": False, "balance": 0, "last_claim_time": 0, 
            "legend_mx_active": False, "daily_code": unique_daily_code, "last_daily_time": 0,
            "claimed_secret_codes": set()
        }

    current_bal = user_stats[user_id]['balance']
    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی یا هێزدارترین سیستەمێ داونلۆدکرنێ!\n\n"
        f"💰 Balance-ێ تە: `{current_bal}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دەستپێکرنێ، لینکێ خۆ بۆ من بنێرە یاخود دوگمەیێن خوارێ بکاربينە!"
    )
    await callback_query.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^mx_video_download_menu"))
async def mx_video_download_menu_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_stats.setdefault(user_id, {"balance": 0})
    bal = user_stats[user_id]["balance"]

    menu_text = (
        "📥 **Mx Video Download Lab (بەشێ داونلۆدکرنا ڤیدیۆیێ):**\n\n"
        "✨ ل ڤێرە تو دشیای لینکێ خۆ بنێری و ڤیدیۆیێ دابەزینی.\n"
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
    
    is_member = await check_user_channel_membership(client, user_id)
    if not is_member:
        await callback_query.answer("❌ بۆ وەرگرتنا خەلاتی، دڤێت پشکدار بی د چەنەلا مە دا: https://t.me/LEGEND_MODS33", show_alert=True)
        return

    current_t = time.time()
    stats = user_stats.setdefault(user_id, {
        "balance": 0, "last_claim_time": 0, "downloads_count": 0, 
        "success_count": 0, "links_count": 0, "rank": "⭐ ئەندامێ نوو", 
        "last_links": [], "bonus_claimed": False, "legend_mx_active": False,
        "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0,
        "claimed_secret_codes": set()
    })
    
    cooldown_period = 3 * 3600
    time_passed = current_t - stats["last_claim_time"]
    
    if time_passed < cooldown_period:
        remaining = int(cooldown_period - time_passed)
        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        await callback_query.answer(f"⏳ چاڤەڕێی {hrs} دەمژمێر و {mins} خولەک بن بۆ وەرگرتنا خەلاتا نوو.", show_alert=True)
        return
        
    stats["last_claim_time"] = current_t
    stats["balance"] += 10
    
    claim_text = (
        "🎁 **پیرۆزە! خەلاتێ 3 ساعتی ب سەرکەفتن هاتە وەرگرتن:**\n\n"
        "✨ **+10 Key** بۆ Balance-ێ تە هاتە زێدەکرن!\n"
        f"💰 Balance-ێ تە یێ نوو: `{stats['balance']}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(claim_text, reply_markup=kb)
    await callback_query.answer("🎉 10 Key ب سەرکەفتن هاتنە زێدکرن!")

@app.on_callback_query(filters.regex(r"^my_profile"))
async def profile_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name or "User"
    user_username = f"@{callback_query.from_user.username}" if callback_query.from_user.username else "نەدیار"

    stats = user_stats.setdefault(user_id, {
        "name": user_name, "username": user_username, "links_count": 0,
        "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو", 
        "last_links": [], "bonus_claimed": False, "balance": 0, "last_claim_time": 0, 
        "legend_mx_active": False, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0,
        "claimed_secret_codes": set()
    })

    profile_text = (
        f"╔═════════════════════════╗\n"
        f"     👤 **پروفایلا تە یێ تڕلیۆنی**     \n"
        f"╚═════════════════════════╝\n\n"
        f"🔹 ناڤ: `{stats['name']}`\n"
        f"• 💰 Balance: `{stats['balance']}` Key\n"
        f"• 🎁 کۆدێ ڕۆژانە (75 Key): `{stats['daily_code']}`\n"
        f"• 📦 لینکێن هنارتی: `{stats['links_count']}`\n"
        f"• 📥 داونلۆد: `{stats['downloads_count']}`\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    
    profile_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 نووکرنا پروفایلی (Refresh)", callback_data="my_profile"),
            InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")
        ],
        [
            InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
        ]
    ])
    
    await callback_query.message.edit_text(profile_text, reply_markup=profile_kb)
    await callback_query.answer("🔄 پروفایلا تە بە خێرایی هاتە نووکرن (Refreshed)!")

@app.on_callback_query(filters.regex(r"^my_downloads"))
async def downloads_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.get(user_id, {"downloads_count": 0, "balance": 0})
    
    dl_text = (
        f"📥 **بەشێ ڤیدیۆیێن داونلۆدكری:**\n\n"
        f"✨ تە **{stats['downloads_count']}** فایل دابەزاندینە.\n"
        f"💰 Balance-ێ مایی: `{stats['balance']}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(dl_text, reply_markup=kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_global_stats"))
async def global_stats_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    total_users = len(user_stats)
    stats_text = (
        f"📊 **ئامارێن گشتی:**\n\n"
        f"👥 کاربەرێن چالاک: `{total_users}`\n"
        f"📥 گشتی داونلۆد: `{global_total_downloads}`\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(stats_text, reply_markup=kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_help"))
async def bot_help_handler(client, callback_query: CallbackQuery):
    help_text = (
        "💡 **رێنمایێن بەکارهۆنانێ:**\n\n"
        "• 75 کۆدێن ڤەشارتى هەنە و هەر کۆدەک **600 Balance** ددەت!\n"
        "• هەر کۆدەک تنێ بۆ **2 کەسان** هاتیە دانان و هەر ID تنێ جارەکێ دکارە بکاربينت.\n"
        "• کۆدێ ڕۆژانەیێ تایبەت یێ کاربەری **75 Key** ددەت.\n"
        "• نرخێ داونلۆدکرنێ بوویە **2 Key**.\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(help_text, reply_markup=kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^system_status"))
async def system_status_handler(client, callback_query: CallbackQuery):
    status_text = "⚙️ **سیستەم ب ڕێکوپێکی کار دکەت.**\n\n👑 خودان: @YUSEEF_SURCHI"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(status_text, reply_markup=kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^daily_bonus"))
async def daily_bonus_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    is_member = await check_user_channel_membership(client, user_id)
    if not is_member:
        await callback_query.answer("❌ بۆ وەرگرتنا خەلاتی، دڤێت پشکدار بی د چەنەلا مە دا: https://t.me/LEGEND_MODS33", show_alert=True)
        return

    current_time = time.time()
    stats = user_stats.setdefault(user_id, {
        "balance": 0, "downloads_count": 0, "success_count": 0, "links_count": 0, 
        "rank": "⭐ ئەندامێ نوو", "last_links": [], "legend_mx_active": False,
        "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0,
        "claimed_secret_codes": set()
    })
    
    cooldown_day = 86400
    if current_time - stats["last_daily_time"] < cooldown_day:
        remaining = int(cooldown_day - (current_time - stats["last_daily_time"]))
        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        await callback_query.answer(f"⏳ خەلاتێ ڕۆژانە تنێ جارەکێ د 24 دەمژمێران دا هێتە وەرگرتن! چاڤەڕێی {hrs} کژمێر و {mins} خولەک بن.", show_alert=True)
        return
        
    stats["last_daily_time"] = current_time
    stats["balance"] += 75
    
    bonus_text = (
        f"🎁 **پیرۆزە! خەلاتێ ڕۆژانە ب سەرکەفتن هاتە وەرگرتن:**\n\n"
        f"✨ **+75 Key** بۆ Balance-ێ تە هاتە زێدەکرن!\n"
        f"🔑 کۆدێ تەیێ تایبەتێ ڕۆژانە: `{stats['daily_code']}`\n"
        f"💰 Balance-ێ نوو: `{stats['balance']}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(bonus_text, reply_markup=kb)
    await callback_query.answer("🎉 75 Key ب سەرکەفتن هاتنە زێدکرن!")

@app.on_callback_query(filters.regex(r"^back_home"))
async def back_home_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name or "User"
    bal = user_stats.setdefault(user_id, {}).get("balance", 0)

    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی یا هێزدارترین سیستەمێ داونلۆدکرنێ یێ جیهانێ!\n\n"
        f"💰 Balance-ێ تە: `{bal}` Key\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دەستپێکرنێ، لینکێ خۆ بۆ من بنێرە یاخود دوگمەیێن خوارێ بکاربينە!"
    )
    await callback_query.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard())
    await callback_query.answer()

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def downloader_core_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.reply_text("❌ تو هاتیە بلۆککرن.")
        return

    is_member = await check_user_channel_membership(client, user_id)
    if not is_member:
        join_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 پشکداربوون د چەنەلێ دا", url="https://t.me/LEGEND_MODS33")],
            [InlineKeyboardButton("🔄 پشکنینا پشکداریێ (Check)", callback_data="check_membership")]
        ])
        await message.reply_text("⚠️ بۆ کارئینانا بۆتی، دڤێت پێش هەمی تشتن پشکدار بی د چەنەلا مە دا: https://t.me/LEGEND_MODS33", reply_markup=join_kb)
        return

    user_name = message.from_user.first_name or "User"
    user_username = f"@{message.from_user.username}" if message.from_user.username else "نەدیار"
    text_input = message.text.strip()
    
    if user_id not in user_stats:
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0, 
            "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو", 
            "last_links": [], "bonus_claimed": False, "balance": 0, "last_claim_time": 0, 
            "legend_mx_active": False, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0,
            "claimed_secret_codes": set()
        }

    if text_input in LEGEND_75_SECRET_CODES:
        if text_input in user_stats[user_id]["claimed_secret_codes"] or user_id in secret_code_usage_count[text_input]:
            await message.reply_text("❌ لێبوورین! تو ڤی کۆدی پێشتر تە وەرگرتیە و هر ID-یەک تنێ جارەکێ دکارە بکاربينت.\n\n👑 خودان: @YUSEEF_SURCHI")
            return
            
        if len(secret_code_usage_count[text_input]) >= 2:
            await message.reply_text("❌ لێبوورین! ئەم کۆدە ڤەشارتىیە و تنێ بۆ **2 کەسان** ب ئەنجام بوو (سنوورێ ڤی کۆدی تەواو بوو).\n\n👑 خودان: @YUSEEF_SURCHI")
            return
            
        secret_code_usage_count[text_input].add(user_id)
        user_stats[user_id]["claimed_secret_codes"].add(text_input)
        
        reward_bal = LEGEND_75_SECRET_CODES[text_input]
        user_stats[user_id]["balance"] += reward_bal
        user_stats[user_id]["legend_mx_active"] = True
        user_stats[user_id]["rank"] = "🔥 LEGEND MX VIP"
        
        await message.reply_text(
            f"🎉 **پیرۆزە! کۆدێ ڤەشارتى یێ `{text_input}` ب سەرکەفتن کارکر:**\n\n"
            f"✨ **+{reward_bal} Balance** بۆ پروفایلا تە هاتە زێدەکرن!\n"
            f"💰 Balance-ێ نوو: `{user_stats[user_id]['balance']}` Key\n\n"
            "👑 خودان: @YUSEEF_SURCHI"
        )
        return

    if text_input == user_stats[user_id]["daily_code"]:
        current_time = time.time()
        cooldown_day = 86400
        if current_time - user_stats[user_id]["last_daily_time"] < cooldown_day:
            remaining = int(cooldown_day - (current_time - user_stats[user_id]["last_daily_time"]))
            hrs = remaining // 3600
            mins = (remaining % 3600) // 60
            await message.reply_text(f"⏳ تە ڤی کۆدی بەدەر وەرگرتیە! چاڤەڕێی {hrs} کژمێر و {mins} خولەک بن.")
            return
            
        user_stats[user_id]["last_daily_time"] = current_time
        user_stats[user_id]["balance"] += 75
        await message.reply_text(
            f"🎁 **پیرۆزە! کۆدێ ڕۆژانە ب سەرکەفتن هاتە کارکرن:**\n\n"
            f"✨ **+75 Key** بۆ Balance-ێ تە هاتە زێدەکرن!\n"
            f"💰 Balance-ێ نوو: `{user_stats[user_id]['balance']}` Key\n\n"
            "👑 خودان: @YUSEEF_SURCHI"
        )
        return

    current_time = time.time()
    if user_id in user_cooldown and current_time - user_cooldown[user_id] < 3:
        await message.reply_text("⚠️ هێدی برا! تنێ ٣ چرکان چاڤەڕێ بکە.")
        return
    user_cooldown[user_id] = current_time

    if not text_input.startswith("http") or not any(x in text_input.lower() for x in ["tiktok", "instagram", "insta.gram", "youtube", "youtu.be", "vm.tiktok", "facebook", "fb.watch", "pinterest"]):
        await message.reply_text(
            "⚠️ لینکێ خەلتە یان کۆدێ نەدروست! هیڤیە لینکەکا دروست یان کۆدەکێ ڕاست بنێرە.\n\n"
            "👑 خودان: @YUSEEF_SURCHI"
        )
        return

    user_stats[user_id]["links_count"] += 1
    url_link = text_input

    process_msg = await message.reply_text("⚡️ زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n👑 خودان: @YUSEEF_SURCHI")

    try:
        ydl_opts = {
            'quiet': True,
            'format': 'best',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
        }
        with YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url_link, download=False)
            vid_title = video_info.get('title', 'Hyper Supreme Media')
            uploader = video_info.get('uploader', 'نەدیار')
            views = video_info.get('view_count', 'نەدیار')
            likes = video_info.get('like_count', 'نەدیار')

        bal = user_stats[user_id]["balance"]
        action_kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📥 داونلۆد MP4 (نرخ: 2 Key)", callback_data=f"dl_mp4|{url_link}"),
                InlineKeyboardButton("🎵 داونلۆد MP3 (نرخ: 2 Key)", callback_data=f"dl_mp3_full|{url_link}")
            ],
            [
                InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")
            ],
            [
                InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
            ]
        ])
        
        await process_msg.edit_text(
            f"📥 **Mx Video Download Lab Info:**\n"
            f"💰 Balance-ێ تە: `{bal}` Key\n\n"
            f"🎬 ناڤێ بابەتی: {vid_title}\n"
            f"👤 خودان: {uploader}\n"
            f"👁 دیتیار: {views} | ❤️ لایک: {likes}\n\n"
            "کوالیتیا خۆ هەڵبژێرە 👇\n\n"
            "👑 خودان: @YUSEEF_SURCHI",
            reply_markup=action_kb
        )
    except Exception as err:
        await process_msg.edit_text(f"❌ هەڵەیەک ڕوویدا:\n`{str(err)}`\n\n👑 خودان: @YUSEEF_SURCHI")

@app.on_callback_query(filters.regex(r"^dl_"))
async def download_callback_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    user_id = callback_query.from_user.id
    
    is_member = await check_user_channel_membership(client, user_id)
    if not is_member:
        await callback_query.answer("❌ بۆ داونلۆدکرنێ، دڤێت پشکدار بی د چەنەلا مە دا: https://t.me/LEGEND_MODS33", show_alert=True)
        return

    data = callback_query.data
    action, url_link = data.split("|", 1)
    
    stats = user_stats.setdefault(user_id, {"balance": 0, "downloads_count": 0, "success_count": 0})
    
    if stats["balance"] < 2:
        await callback_query.answer("❌ Balance-ێ تە نەهنگە! پێدڤییە حداقل 2 Key هەبت.", show_alert=True)
        return

    stats["balance"] -= 2  # کێمکرنا 2 Key بۆ داونلۆدکرنێ
    await callback_query.answer("📥 داونلۆدکرن دەست پێکر (2 Key هاتە کێمکرن)...", show_alert=False)
    status_msg = await callback_query.message.reply_text(f"⏳ خەریکە فایلێ دابەزینم... (Balance: {stats['balance']} Key)\n\n👑 خودان: @YUSEEF_SURCHI")

    filename = None
    try:
        os.makedirs("downloads", exist_ok=True)
        if action == "dl_mp4":
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'quiet': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_link, download=True)
                filename = ydl.prepare_filename(info)
                if not filename.endswith('.mp4'):
                    filename = os.path.splitext(filename)[0] + '.mp4'

            finish_kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
                [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
            ])
            await callback_query.message.reply_video(video=filename, caption=f"🎬 MP4 هاتە داونلۆدکرن!\n💰 Balance: {stats['balance']} Key", reply_markup=finish_kb)
            
        elif action == "dl_mp3_full":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'quiet': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_link, download=True)
                filename = ydl.prepare_filename(info)

            audio_title = info.get('title', 'Full Song')
            finish_kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
                [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
            ])
            await callback_query.message.reply_audio(audio=filename, title=audio_title, performer="YUSEEF_SURCHI", caption=f"🎶 MP3 هاتە داونلۆدکرن!\n💰 Balance: {stats['balance']} Key", reply_markup=finish_kb)

        stats["downloads_count"] += 1
        stats["success_count"] += 1
        global_total_downloads += 1

        if filename and os.path.exists(filename):
            os.remove(filename)
        await status_msg.delete()
    except Exception as e:
        stats["balance"] += 2  # ڤەگەراندنا Key ئەگەر هەڵە هەبت
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        await status_msg.edit_text(f"❌ هەڵەیەک ڕوویدا، Key هاتە ڤەگەراندن:\n`{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI")

print("🚀 Ultimate Supreme Trillion Menu Bot (V25 - 0 Start, 2 Key Download, Channel Join Guard, 3h Reward) with Owner @YUSEEF_SURCHI is Running!")
app.run()
