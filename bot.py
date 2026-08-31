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
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

app = Client(
    "supreme_trillion_ultimate_v21_surchi_mx",
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

# 21 کۆدێن ڕۆژانە یێن جودا و تایبەت ژ 24 دەستپێدکەن (24 تا 44) ب پێکهاتەیا LEGEND-MX-
LEGEND_DAILY_CODES = {
    f"LEGEND-MX-{i}": 20 for i in range(24, 45)
}

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
            InlineKeyboardButton("📊 ئامارێن گشتی یێن بۆتی", callback_data="bot_global_stats"),
            InlineKeyboardButton("💡 رێنمایێن بەکارهۆنانێ", callback_data="bot_help")
        ],
        [
            InlineKeyboardButton("⚙️ سیستەم و پشکنین", callback_data="system_status"),
            InlineKeyboardButton("🎁 خەلاتێن ڕۆژانە (کۆدێ تایبەت)", callback_data="daily_bonus")
        ],
        [
            InlineKeyboardButton("👑 خودان و دامەزرێنەر: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
        ]
    ])

@app.on_message(filters.command("start"))
async def start_command_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.reply_text("❌ لێبوورین، تو هاتیە بلۆککرن ژ کارئینانا ڤی بۆتی.")
        return

    user_name = message.from_user.first_name or "User"
    user_username = f"@{message.from_user.username}" if message.from_user.username else "نەدیار"
    text_content = message.text or ""

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
            "balance": 0,
            "last_claim_time": 0,
            "last_daily_time": 0,
            "legend_mx_active": False,
            "daily_code": unique_daily_code,
            "claimed_legend_codes": set()
        }

    if "LEGEND-MX-BALANCE-600" in text_content or "LEGEND-MX-BALNCE-600" in text_content:
        user_stats[user_id]["balance"] += 600
        user_stats[user_id]["legend_mx_active"] = True
        user_stats[user_id]["rank"] = "🔥 LEGEND MX VIP"
        await message.reply_text("🎉 پیرۆزە! کۆدێ نهێنیێ **LEGEND-MX-BALANCE-600** کارکر و **600 Balance** بو پروفایلا تە هاتە زێدەکرن!")

    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی یا هێزدارترین سیستەمێ داونلۆدکرنێ یێ جیهانێ ب ناڤێ ڕاستەقینە!\n\n"
        f"💰 Balance-ێ تە یێ نها: `{user_stats[user_id]['balance']}` Key\n"
        f"🎁 کۆدێ خەلاتێ ڕۆژانەیێ تە: `{user_stats[user_id]['daily_code']}`\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دابەزاندنێ، تنێ لینکێ خۆ ل ڤێرە بنێرە!"
    )
    
    await message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

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
    current_t = time.time()
    
    stats = user_stats.setdefault(user_id, {
        "balance": 0, "last_claim_time": 0, "downloads_count": 0, 
        "success_count": 0, "links_count": 0, "rank": "⭐ ئەندامێ نوو", 
        "last_links": [], "bonus_claimed": False, "legend_mx_active": False,
        "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0,
        "claimed_legend_codes": set()
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
        "claimed_legend_codes": set()
    })

    profile_text = (
        f"╔═════════════════════════╗\n"
        f"     👤 **پروفایلا تە یێ تڕلیۆنی**     \n"
        f"╚═════════════════════════╝\n\n"
        f"🔹 ناڤ: `{stats['name']}`\n"
        f"• 💰 Balance: `{stats['balance']}` Key\n"
        f"• 🎁 کۆدێ خەلاتێ ڕۆژانە: `{stats['daily_code']}`\n"
        f"• 📦 لینکێن هنارتی: `{stats['links_count']}`\n"
        f"• 📥 داونلۆد: `{stats['downloads_count']}`\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    
    profile_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 نووکرنا پروفایلی", callback_data="my_profile"),
            InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")
        ],
        [
            InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
        ]
    ])
    
    await callback_query.message.edit_text(profile_text, reply_markup=profile_kb)
    await callback_query.answer()

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
        "• بۆ وەرگرتنا خەلاتێ ڕۆژانە، تو دشیای کۆدێن LEGEND-MX- (ژ 24 تا 44) یاخود کۆدێ خۆ یێ تایبەت بنێری و 20 Key وەرگری!\n"
        "• هەر کۆدەک ژ وان 21 کۆدان دشێت ئێکجار بکاربێ بۆ هر کاربەری.\n\n"
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
    current_time = time.time()
    
    stats = user_stats.setdefault(user_id, {
        "balance": 0, "downloads_count": 0, "success_count": 0, "links_count": 0, 
        "rank": "⭐ ئەندامێ نوو", "last_links": [], "legend_mx_active": False,
        "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0,
        "claimed_legend_codes": set()
    })
    
    cooldown_day = 86400
    if current_time - stats["last_daily_time"] < cooldown_day:
        remaining = int(cooldown_day - (current_time - stats["last_daily_time"]))
        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        await callback_query.answer(f"⏳ خەلاتێ ڕۆژانە تنێ جارەکێ د 24 دەمژمێران دا هێتە وەرگرتن! چاڤەڕێی {hrs} کژمێر و {mins} خولەک بن.", show_alert=True)
        return
        
    stats["last_daily_time"] = current_time
    stats["balance"] += 20
    
    bonus_text = (
        f"🎁 **پیرۆزە! خەلاتێ ڕۆژانە ب سەرکەفتن هاتە وەرگرتن:**\n\n"
        f"✨ **+20 Key** بۆ Balance-ێ تە هاتە زێدەکرن!\n"
        f"🔑 کۆدێ تەیێ تایبەتێ ڕۆژانە: `{stats['daily_code']}`\n"
        f"💰 Balance-ێ نوو: `{stats['balance']}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(bonus_text, reply_markup=kb)
    await callback_query.answer("🎉 20 Key ب سەرکەفتن هاتنە زێدکرن!")

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

    user_name = message.from_user.first_name or "User"
    user_username = f"@{message.from_user.username}" if message.from_user.username else "نەدیار"
    text_input = message.text.strip()
    
    if user_id not in user_stats:
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0, 
            "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو", 
            "last_links": [], "bonus_claimed": False, "balance": 0, "last_claim_time": 0, 
            "legend_mx_active": False, "daily_code": f"MX-DAY-{user_id}-{random.randint(1000, 9999)}", "last_daily_time": 0,
            "claimed_legend_codes": set()
        }

    # پشکنینا کۆدێ تایبەت یێ کاربەری
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
        user_stats[user_id]["balance"] += 20
        await message.reply_text(
            f"🎁 **پیرۆزە! کۆدێ ڕۆژانە ب سەرکەفتن هاتە کارکرن:**\n\n"
            f"✨ **+20 Key** بۆ Balance-ێ تە هاتە زێدەکرن!\n"
            f"💰 Balance-ێ نوو: `{user_stats[user_id]['balance']}` Key\n\n"
            "👑 خودان: @YUSEEF_SURCHI"
        )
        return

    # پشکنینا 21 کۆدێن LEGEND-MX- (ژ 24 تا 44)
    if text_input in LEGEND_DAILY_CODES:
        if text_input in user_stats[user_id]["claimed_legend_codes"]:
            await message.reply_text("❌ تو ڤی کۆدی پێشتر تە وەرگرتیە و تنێ جارەکێ دکارى بکاربيني!\n\n👑 خودان: @YUSEEF_SURCHI")
            return
            
        user_stats[user_id]["claimed_legend_codes"].add(text_input)
        reward_keys = LEGEND_DAILY_CODES[text_input]
        user_stats[user_id]["balance"] += reward_keys
        await message.reply_text(
            f"🎉 **پیرۆزە! کۆدێ `{text_input}` ب سەرکەفتن کارکر:**\n\n"
            f"✨ **+{reward_keys} Key** بۆ Balance-ێ تە هاتە زێدەکرن!\n"
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
                InlineKeyboardButton("📥 داونلۆد MP4 (نرخ: 1 Key)", callback_data=f"dl_mp4|{url_link}"),
                InlineKeyboardButton("🎵 داونلۆد MP3 (نرخ: 1 Key)", callback_data=f"dl_mp3_full|{url_link}")
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
    data = callback_query.data
    action, url_link = data.split("|", 1)
    
    stats = user_stats.setdefault(user_id, {"balance": 0, "downloads_count": 0, "success_count": 0})
    
    if stats["balance"] < 1:
        await callback_query.answer("❌ Balance-ێ تە نەهنگە! پێدڤییە حداقل 1 Key هەبت.", show_alert=True)
        return

    stats["balance"] -= 1
    await callback_query.answer("📥 داونلۆدکرن دەست پێکر (1 Key هاتە کێمکرن)...", show_alert=False)
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
        stats["balance"] += 1
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        await status_msg.edit_text(f"❌ هەڵەیەک ڕوویدا، Key هاتە ڤەگەراندن:\n`{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI")

print("🚀 Ultimate Supreme Trillion Menu Bot (V21 - 21 Unique Daily Codes Edition) with Owner @YUSEEF_SURCHI is Running!")
app.run()
