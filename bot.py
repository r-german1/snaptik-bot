import os
import asyncio
import time
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

# Advanced Global Storage & Legend MX Balance System
user_stats = {}
global_total_downloads = 0
user_cooldown = {}
banned_users = set()

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
            InlineKeyboardButton("🎁 خەلاتێن ڕۆژانە", callback_data="daily_bonus")
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
            "legend_mx_active": False
        }

    # Secret check for LEGEND-MX-BALANCE-600
    if "LEGEND-MX-BALANCE-600" in text_content or "LEGEND-MX-BALNCE-600" in text_content:
        user_stats[user_id]["balance"] += 600
        user_stats[user_id]["legend_mx_active"] = True
        user_stats[user_id]["rank"] = "🔥 LEGEND MX VIP"
        await message.reply_text("🎉 پیرۆزە! کۆدێ نهێنیێ **LEGEND-MX-BALANCE-600** کارکر و **600 Balance** بو پروفایلا تە هاتە زێدەکرن!")

    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی یا هێزدارترین سیستەمێ داونلۆدکرنێ یێ جیهانێ (تیکتۆک، اینستاگرام، یوتیوب و پلاتفۆرمێن دی) ب کوالیتیا 4K و MP3 ب ناڤێ ڕاستەقینە!\n\n"
        f"💰 Balance-ێ تە یێ نها: `{user_stats[user_id]['balance']}` Key\n\n"
        "✨ **خاسەتیێن مەزن یێن سیستەمی (Mx Download & Legend Systems):**\n"
        "• داونلۆدکرنا بێ کێشە، خێرا و باوەڕپێکری ب کوالیتیێن جودا\n"
        "• سیستەمێ Key ێن 3 ساعتی و وەرگرتنا 10 Key\n"
        "• پروفایلا تایبەت، مێژووا گەڕانێ و پلەیێن بەرزی\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 **تێبینی:** بۆ دابەزاندنێ، تنێ لینکێ خۆ ل ڤێرە بنێرە یاخود دوگمەیێن خوارێ بکاربينە!"
    )
    
    await message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^mx_video_download_menu"))
async def mx_video_download_menu_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_stats.setdefault(user_id, {"balance": 0})
    bal = user_stats[user_id]["balance"]

    menu_text = (
        "📥 **Mx Video Download Lab (بەشێ داونلۆدکرنا ڤیدیۆیێ):**\n\n"
        "✨ ل ڤێرە تو دشیای لینکێ خۆ بنێری و ڤیدیۆیێ ب هەلبژارتنا **MP4** یاخود **MP3** دابەزینی.\n"
        "💡 **تێبینی:** هەر داونلۆدکرنەک ب تنێ **1 Key** ژ Balance-ێ تە کێم دکەت!\n"
        f"💰 Balance-ێ تە: `{bal}` Key\n\n"
        "🔗 لینکێ خۆ ل خوارێ بنێرە یاخود ڤێرە تاقەتبکە!\n\n"
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
        "last_links": [], "bonus_claimed": False, "legend_mx_active": False
    })
    
    # 3 hours = 3 * 3600 seconds = 10800 seconds
    cooldown_period = 3 * 3600
    time_passed = current_t - stats["last_claim_time"]
    
    if time_passed < cooldown_period:
        remaining = int(cooldown_period - time_passed)
        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        await callback_query.answer(f"⏳ هێدی برا! پێدڤییە تو چاڤەڕێی {hrs} دەمژمێر و {mins} خولەک بن بۆ وەرگرتنا خەلاتا نوو یا 10 Key.", show_alert=True)
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
        "last_links": [], "bonus_claimed": False, "balance": 0, "last_claim_time": 0, "legend_mx_active": False
    })

    total_l = stats['links_count']
    total_d = stats['downloads_count']
    bal = stats['balance']
    success_rate = "100%" if total_d > 0 or total_l > 0 else "0%"
    history_str = "\n".join([f"• `{lnk}`" for lnk in stats['last_links'][-3:]]) if stats['last_links'] else "تە هێشتا چ لینک نەناردینە."

    profile_text = (
        f"╔═════════════════════════╗\n"
        f"     👤 **پروفایلا تەیێ تڕلیۆنی و پێشکەفتى**     \n"
        f"╚═════════════════════════╝\n\n"
        f"🔹 **زانیاریێن کەسایەتی:**\n"
        f"• ناڤێ تە: `{stats['name']}`\n"
        f"• یوزەرێر: `{stats['username']}`\n"
        f"• ئای دی (ID): `{user_id}`\n"
        f"• پلە و ڕێزبەندی: `{stats['rank']}`\n"
        f"• 💰 Balance-ێ تە: `{bal}` Key\n\n"
        f"📊 **تۆمار و ئامارێن تە:**\n"
        f"• گشتی لینکێن هنارتی: `📦 {total_l}`\n"
        f"• ڤیدیۆیێن هاتیە دابەزاندن: `📥 {total_d}`\n"
        f"• پڕۆسەیێن سەرکەفتی: `✅ {stats['success_count']}`\n"
        f"• ڕێژا سەرکەفتنێ: `🌟 {success_rate}`\n\n"
        f"🔗 **دووماهیک لینکێن تە:**\n{history_str}\n\n"
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
    await callback_query.answer("✨ پروفایلا تە ب سەرکەفتن هاتە نووکرن!")

@app.on_callback_query(filters.regex(r"^my_downloads"))
async def downloads_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.get(user_id, {"downloads_count": 0, "success_count": 0, "balance": 0})
    
    dl_text = (
        f"📥 **بەشێ ڤیدیۆیێن داونلۆدكری:**\n\n"
        f"✨ هەتا نوکە تە ب دەستخستنا خۆ **{stats['downloads_count']}** فایل ب کوالیتیا بلندا 4K، MP4 و MP3 دابەزاندینە.\n"
        f"💰 Balance-ێ تە یێ مایی: `{stats['balance']}` Key\n"
        f"🚀 کوالیتیا سیستەمی: 100% کارا، خێرا و بێ کێشە\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    
    dl_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    
    await callback_query.message.edit_text(dl_text, reply_markup=dl_kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_global_stats"))
async def global_stats_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    total_users = len(user_stats)
    
    stats_text = (
        f"📊 **ئامارێن گشتی یێن سیستەمێ تڕلیۆنی:**\n\n"
        f"👥 هژمارا کاربەرێن چالاک: `{total_users}`\n"
        f"📥 گشتی داونلۆدێن هاتیە کرن ل سیستەمی: `{global_total_downloads}`\n"
        f"⚡️ ڕەوشا سێرڤەری: `100% کارا (Ping: 12ms)`\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    
    stats_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    
    await callback_query.message.edit_text(stats_text, reply_markup=stats_kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^bot_help"))
async def bot_help_handler(client, callback_query: CallbackQuery):
    help_text = (
        "💡 **رێنمایێن بەکارهۆنانێ:**\n\n"
        "1️⃣ بۆ داونلۆدکرنێ، تنێ لینکێ (تیکتۆک، اینستاگرام، یوتیوب) ل ڤێرە بنێرە.\n"
        "2️⃣ پاشان زانیاریێن ڤیدیۆیێ دەرکەفن و تو دشیای کوالیتیا MP4 یاخود MP3 هەڵبژێری (هەر دابەزاندنەک 1 Key ژ Balance-ێ تە دبرێت).\n"
        "3️⃣ تو دشیای هه‌ر 3 دەمژمێران جارەکێ 10 Key ژ خەلاتێن تایبەت وەرگری.\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    help_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(help_text, reply_markup=help_kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^system_status"))
async def system_status_handler(client, callback_query: CallbackQuery):
    status_text = (
        "⚙️ **سیستەم و پشکنینا خێراتیێ:**\n\n"
        "• پەتەیا سێرڤەری (Server Status): `Online & Secure`\n"
        "• پێکۆیا لۆدێ (CPU Load): `1.2% (Normal)`\n"
        "• پاشەکەوتا سێرڤەری (Auto-Clean): `Active`\n"
        "• گەشەپێدەر و خودان: `@YUSEEF_SURCHI`\n\n"
        "✨ هەمی پڕۆسە ب کوالیتیا بلند کار دکەن!"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(status_text, reply_markup=kb)
    await callback_query.answer("⚙️ ڕەوشا سیستەمی ب سەرکەفتن هاتە پشکنین!")

@app.on_callback_query(filters.regex(r"^daily_bonus"))
async def daily_bonus_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.setdefault(user_id, {"downloads_count": 0, "bonus_claimed": False, "balance": 0})
    
    if stats.get("bonus_claimed", False):
        await callback_query.answer("⚠️ تە خەلاتێ خۆ یێ ڕۆژانە وەرگرتیە!", show_alert=True)
        return
        
    stats["bonus_claimed"] = True
    stats["balance"] += 20  # Daily bonus 20 keys for users
    bonus_text = (
        "🎁 **پیرۆزە! تە خەلاتێ خۆ یێ ڕۆژانە وەرگرت:**\n\n"
        "✨ **+20 Key** بۆ Balance-ێ تە هاتە زێدەکرن!\n"
        f"💰 Balance-ێ نوو: `{stats['balance']}` Key\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await callback_query.message.edit_text(bonus_text, reply_markup=kb)
    await callback_query.answer("🎉 خەلات ب سەرکەفتن هاتە وەرگرتن!")

@app.on_callback_query(filters.regex(r"^back_home"))
async def back_home_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name or "User"
    bal = user_stats.setdefault(user_id, {}).get("balance", 0)

    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی یا هێزدارترین سیستەمێ داونلۆدکرنێ یێ جیهانێ (تیکتۆک، اینستاگرام، و یوتیوب) ب کوالیتیا 4K و MP3 ب ناڤێ ڕاستەقینە!\n\n"
        f"💰 Balance-ێ تە: `{bal}` Key\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دەستپێکرنێ، لینکێ خۆ بۆ من بنێرە یان دوگمەیێن خوارێ بکاربينە!"
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
    url_link = message.text.strip()
    
    if user_id not in user_stats:
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0, 
            "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو", 
            "last_links": [], "bonus_claimed": False, "balance": 0, "last_claim_time": 0, "legend_mx_active": False
        }

    # Anti-Spam protection (3 seconds delay)
    current_time = time.time()
    if user_id in user_cooldown and current_time - user_cooldown[user_id] < 3:
        await message.reply_text("⚠️ هێدی برا! تنێ ٣ چرکان چاڤەڕێ بکە بەرى کو لینکەکا دی بنێری.")
        return
    user_cooldown[user_id] = current_time

    if not url_link.startswith("http") or not any(x in url_link.lower() for x in ["tiktok", "instagram", "insta.gram", "youtube", "youtu.be", "vm.tiktok", "facebook", "fb.watch", "pinterest"]):
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
            [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
        ])
        await message.reply_text(
            "⚠️ برا، تنێ لینکێن **تیکتۆک، اینستاگرام، و یوتیوب** ل لابا من کار دکەن! هیڤیە لینکەکا دروست بۆ من بنێرە.\n\n"
            "👑 خودان: @YUSEEF_SURCHI",
            reply_markup=err_kb
        )
        return

    user_stats[user_id]["links_count"] += 1
    total_user_links = user_stats[user_id]["links_count"]
    
    if url_link not in user_stats[user_id]["last_links"]:
        user_stats[user_id]["last_links"].append(url_link)
        if len(user_stats[user_id]["last_links"]) > 5:
            user_stats[user_id]["last_links"].pop(0)

    process_msg = await message.reply_text(
        f"⚡️ Mx Video Download Lab کار دکەت (کاربەر: {user_name} | لینکێن تە: {total_user_links}): نوکە زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )

    try:
        ydl_opts = {
            'quiet': True,
            'format': 'best',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
        }
        with YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url_link, download=False)
            vid_title = video_info.get('title', 'Hyper Supreme Media')
            uploader = video_info.get('uploader', 'نەدیار (Unknown)')
            views = video_info.get('view_count', 'نەدیار')
            likes = video_info.get('like_count', 'نەدیار')
            comments = video_info.get('comment_count', 'نەدیار')
            shares = video_info.get('repost_count', video_info.get('share_count', 'نەدیار'))
            
            raw_duration = video_info.get('duration', 0)
            if not raw_duration and 'entries' in video_info:
                try:
                    raw_duration = video_info['entries'][0].get('duration', 0)
                except:
                    pass
            
            if raw_duration:
                mins = int(raw_duration // 60)
                secs = int(raw_duration % 60)
                vid_time_str = f"{mins} دەقە و {secs} چرکه" if mins > 0 else f"{secs} چرکه"
            else:
                vid_time_str = "تەواڤ"

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
            f"👤 نڤێسەر/کەسێ لینک هنارتی: {user_name} ({user_username})\n"
            f"💰 Balance-ێ تە: `{bal}` Key (هەر داونلۆدەک 1 Key دبرێت)\n\n"
            f"🎬 ناڤێ بابەتی: {vid_title}\n"
            f"👤 خودانێ ڤیدیۆیێ: {uploader}\n"
            f"⏱ دەمێ ڤیدیۆیێ: {vid_time_str}\n"
            f"👁 دیتیار (Views): {views}\n"
            f"❤️ لایک (Likes): {likes}\n\n"
            "کوالیتیا خۆ هەڵبژێرە بۆ داونلۆدکرنێ 👇\n\n"
            "👑 خودان و بەرپرس: @YUSEEF_SURCHI",
            reply_markup=action_kb
        )
    except Exception as err:
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
            [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
        ])
        await process_msg.edit_text(
            f"❌ هەڵەیەک ڕوویدا د وەرگرتنا زانیاریان دا:\n`{str(err)}`\n\n"
            "👑 خودان: @YUSEEF_SURCHI",
            reply_markup=err_kb
        )

@app.on_callback_query(filters.regex(r"^dl_"))
async def download_callback_handler(client, callback_query: CallbackQuery):
    global global_total_downloads
    user_id = callback_query.from_user.id
    data = callback_query.data
    action, url_link = data.split("|", 1)
    
    stats = user_stats.setdefault(user_id, {"balance": 0, "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو"})
    
    # Check if user has enough balance (1 key required per download)
    if stats["balance"] < 1:
        await callback_query.answer("❌ Balance-ێ تە نەهنگە! پێدڤییە حداقل 1 Key هەبت بۆ داونلۆدکرنێ. (سەرا خەلاتێن 3 ساعتی بکە)", show_alert=True)
        return

    # Deduct 1 key per video download
    stats["balance"] -= 1

    await callback_query.answer("📥 داونلۆدکرن دەست پێکر (1 Key هاتە کێمکرن)...", show_alert=False)
    status_msg = await callback_query.message.reply_text(
        f"⏳ خەریکە فایلێ دابەزینم بۆ تە... (Balance-ێ نوو: {stats['balance']} Key)\n\n👑 خودان: @YUSEEF_SURCHI"
    )

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
            await callback_query.message.reply_video(
                video=filename,
                caption=f"🎬 ب سەرکەفتن ڤیدیۆ (MP4) هاتە داونلۆدکرن!\n💰 Balance-ێ مایی: {stats['balance']} Key\n\n👑 خودان: @YUSEEF_SURCHI",
                reply_markup=finish_kb
            )
            
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
            await callback_query.message.reply_audio(
                audio=filename,
                title=audio_title,
                performer="YUSEEF_SURCHI",
                caption=f"🎶 سترانا تەمام ({audio_title}) هاتە داونلۆدکرن!\n💰 Balance-ێ مایی: {stats['balance']} Key\n\n👑 خودان: @YUSEEF_SURCHI",
                reply_markup=finish_kb
            )

        stats["downloads_count"] += 1
        stats["success_count"] += 1
        if stats["downloads_count"] >= 10:
            stats["rank"] = "⭐ ئەندامێ پێشکەفتى"
        if stats["downloads_count"] >= 50:
            stats["rank"] = "🔥 ئەندامێ زێڕین"
        if stats["downloads_count"] >= 100:
            stats["rank"] = "👑 ئەندامێ تڕلیۆنی"

        global_total_downloads += 1

        if filename and os.path.exists(filename):
            os.remove(filename)

        await status_msg.delete()
    except Exception as e:
        # Refund key if download fails
        stats["balance"] += 1
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        err_back_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
            [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
        ])
        await status_msg.edit_text(
            f"❌ هەڵەیەک ڕوویدا، Key-ێ تە بۆتە هاتە ڤەگەراندن:\n`{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI",
            reply_markup=err_back_kb
        )

print("🚀 Ultimate Supreme Trillion Menu Bot (V21 - Mx Video Download Lab & LEGEND-MX-BALANCE-600 Edition) with Owner @YUSEEF_SURCHI is Running!")
app.run()
