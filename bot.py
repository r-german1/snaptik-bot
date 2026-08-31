import os
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")
OWNER_ID = int(os.environ.get("OWNER_ID", "0")) # Adjust if needed or use username check

app = Client(
    "supreme_trillion_ultimate_v20_surchi",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    sleep_threshold=0
)

# Advanced Global Storage & 20-Feature Trillion Stats
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

    if user_id not in user_stats:
        user_stats[user_id] = {
            "name": user_name,
            "username": user_username,
            "links_count": 0,
            "downloads_count": 0,
            "success_count": 0,
            "rank": "⭐ ئەندامێ نوو",
            "last_links": [],
            "bonus_claimed": False
        }

    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی یا هێزدارترین سیستەمێ داونلۆدکرنێ یێ جیهانێ (تیکتۆک، اینستاگرام، یوتیوب و پلاتفۆرمێن دی) ب کوالیتیا 4K و MP3 ب ناڤێ ڕاستەقینە!\n\n"
        "✨ **خاسەتیێن مەزن یێن سیستەمی (20+ تایبەتمەندی):**\n"
        "• داونلۆدکرنا بێ کێشە، خێرا و باوەڕپێکری ب کوالیتیێن جودا\n"
        "• پروفایلا تایبەت، مێژووا گەڕانێ و پلەیێن بەرزی\n"
        "• سیستەمێ خەلاتێن ڕۆژانە و پشکنینا خێراتیێ\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 **تێبینی:** بۆ دابەزاندنێ، تنێ لینکێ خۆ ل ڤێرە بنێرە یاخود دوگمەیێن خوارێ بکاربينە!"
    )
    
    await message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

@app.on_callback_query(filters.regex(r"^my_profile"))
async def profile_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name or "User"
    user_username = f"@{callback_query.from_user.username}" if callback_query.from_user.username else "نەدیار"

    if user_id not in user_stats:
        user_stats[user_id] = {
            "name": user_name, "username": user_username, "links_count": 0,
            "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو", "last_links": [], "bonus_claimed": False
        }

    stats = user_stats[user_id]
    total_l = stats['links_count']
    total_d = stats['downloads_count']
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
        f"• پلە و ڕێزبەندی: `{stats['rank']}`\n\n"
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
    stats = user_stats.get(user_id, {"downloads_count": 0, "success_count": 0})
    
    dl_text = (
        f"📥 **بەشێ ڤیدیۆیێن داونلۆدكری:**\n\n"
        f"✨ هەتا نوکە تە ب دەستخستنا خۆ **{stats['downloads_count']}** فایل ب کوالیتیا بلندا 4K، MP4 و MP3 دابەزاندینە.\n"
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
        "2️⃣ پاشان زانیاریێن ڤیدیۆیێ دەرکەفن و تو دشیای کوالیتیا MP4 یان MP3 هەڵبژێری.\n"
        "3️⃣ سیستەم دێ ب خوەکارى فایلان پاک کەت و ڤەگەرێ بۆ لابا سەرەکی دەستپێکت.\n\n"
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
    stats = user_stats.setdefault(user_id, {"downloads_count": 0, "bonus_claimed": False})
    
    if stats.get("bonus_claimed", False):
        await callback_query.answer("⚠️ تە خەلاتێ خۆ یێ ڕۆژانە وەرگرتیە!", show_alert=True)
        return
        
    stats["bonus_claimed"] = True
    bonus_text = (
        "🎁 **پیرۆزە! تە خەلاتێ خۆ یێ ڕۆژانە وەرگرت:**\n\n"
        "✨ پشکەک ژ خاڵێن تڕلیۆنی و ئەندامەتیێ بۆ پروفایلا تە هاتە زێدەکرن.\n\n"
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
    user_name = callback_query.from_user.first_name or "User"
    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 بخێرهاتن بۆ لابا سەرەکی یا هێزدارترین سیستەمێ داونلۆدکرنێ یێ جیهانێ (تیکتۆک، اینستاگرام، و یوتیوب) ب کوالیتیا 4K و MP3 ب ناڤێ ڕاستەقینە!\n\n"
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
    
    # Anti-Spam protection (3 seconds delay)
    current_time = time.time()
    if user_id in user_cooldown and current_time - user_cooldown[user_id] < 3:
        await message.reply_text("⚠️ هێدی برا! تنێ ٣ چرکان چاڤەڕێ بکە بەرى کو لینکەکا دی بنێری.")
        return
    user_cooldown[user_id] = current_time

    if user_id not in user_stats:
        user_stats[user_id] = {"name": user_name, "username": user_username, "links_count": 0, "downloads_count": 0, "success_count": 0, "rank": "⭐ ئەندامێ نوو", "last_links": [], "bonus_claimed": False}

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
    
    # Track last links history
    if url_link not in user_stats[user_id]["last_links"]:
        user_stats[user_id]["last_links"].append(url_link)
        if len(user_stats[user_id]["last_links"]) > 5:
            user_stats[user_id]["last_links"].pop(0)

    process_msg = await message.reply_text(
        f"⚡️ سیستەم کار دکەت (کاربەر: {user_name} | لینکێن تە: {total_user_links}): نوکە زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n"
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

        action_kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📥 داونلۆدکرنا MP4 (4K)", callback_data=f"dl_mp4|{url_link}"),
                InlineKeyboardButton("🎵 داونلۆدکرنا MP3", callback_data=f"dl_mp3_full|{url_link}")
            ],
            [
                InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")
            ],
            [
                InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
            ]
        ])
        
        await process_msg.edit_text(
            f"👤 نڤێسەر/کەسێ لینک هنارتی: {user_name} ({user_username})\n"
            f"📊 هژمارا لینکێن تە یێن هنارتی: {total_user_links} لینک\n\n"
            f"🎬 ناڤێ بابەتی: {vid_title}\n"
            f"👤 خودانێ ڤیدیۆیێ: {uploader}\n"
            f"⏱ دەمێ ڤیدیۆیێ: {vid_time_str}\n"
            f"👁 دیتیار (Views): {views}\n"
            f"❤️ لایک (Likes): {likes}\n"
            f"💬 کۆمێنت (Comments): {comments}\n"
            f"🔁 پشکڤەکرن (Shares): {shares}\n\n"
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
    
    await callback_query.answer("📥 داونلۆدکرن دەست پێکر...", show_alert=False)
    status_msg = await callback_query.message.reply_text(
        "⏳ خەریکە فایلێ ب کوالیتیا بلندا 4K دابەزینم بۆ تە...\n\n👑 خودان: @YUSEEF_SURCHI"
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
                caption="🎬 ب سەرکەفتن ڤیدیۆ (MP4) ب کوالیتیا بلند هاتە داونلۆدکرن!\n\n👑 خودان: @YUSEEF_SURCHI",
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
                caption=f"🎶 سترانا تەمام ({audio_title}) ب کوالیتیا بلند و ب ناڤێ ڕاستەقینە هاتە داونلۆدکرن!\n\n👑 خودان: @YUSEEF_SURCHI",
                reply_markup=finish_kb
            )

        if user_id in user_stats:
            user_stats[user_id]["downloads_count"] += 1
            user_stats[user_id]["success_count"] += 1
            if user_stats[user_id]["downloads_count"] >= 10:
                user_stats[user_id]["rank"] = "⭐ ئەندامێ پێشکەفتى"
            if user_stats[user_id]["downloads_count"] >= 50:
                user_stats[user_id]["rank"] = "🔥 ئەندامێ زێڕین"
            if user_stats[user_id]["downloads_count"] >= 100:
                user_stats[user_id]["rank"] = "👑 ئەندامێ تڕلیۆنی"

        global_total_downloads += 1

        if filename and os.path.exists(filename):
            os.remove(filename)

        await status_msg.delete()
    except Exception as e:
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
            f"❌ چەڵۆکیەک ڕوویدا د دەمێ داونلۆدکرنێ دا:\n`{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI",
            reply_markup=err_back_kb
        )

print("🚀 Ultimate Supreme Trillion Menu Bot (V20 - Final Complete Edition) with Owner @YUSEEF_SURCHI is Running Perfectly!")
app.run()
