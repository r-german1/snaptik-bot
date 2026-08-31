import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")

app = Client(
    "supreme_advanced_profile_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    sleep_threshold=0
)

# Advanced User Stats & Profile Storage Dictionary
user_stats = {}
global_total_downloads = 0

@app.on_message(filters.command("start"))
async def start_command_handler(client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"
    user_username = f"@{message.from_user.username}" if message.from_user.username else "نەدیار"

    if user_id not in user_stats:
        user_stats[user_id] = {
            "name": user_name,
            "username": user_username,
            "links_count": 0,
            "downloads_count": 0,
            "success_count": 0,
            "rank": "ئەندامێ چالاک"
        }

    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 ئەڤە هێزدارترین سیستەمێ داونلۆدکرنێ یێ بێ وێنە (تیکتۆک، اینستاگرام، و یوتیوب) ب کوالیتیا هەرە بلندا 4K و MP3 ب ناڤێ ڕاستەقینە!\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دەستپێکرنێ، لینکێ خۆ بۆ من بنێرە یان دوگمەیێن خوارێ بکاربينە!"
    )
    
    welcome_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 پروفایلا پێشکەفتى", callback_data="my_profile"),
            InlineKeyboardButton("📥 ڤیدیۆیێن داونلۆدکري", callback_data="my_downloads")
        ],
        [
            InlineKeyboardButton("📊 ئامارێن گشتی یێن بۆتی", callback_data="bot_global_stats")
        ],
        [
            InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
        ]
    ])
    await message.reply_text(welcome_text, reply_markup=welcome_kb)

@app.on_callback_query(filters.regex(r"^my_profile"))
async def profile_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name or "User"
    user_username = f"@{callback_query.from_user.username}" if callback_query.from_user.username else "نەدیار"

    if user_id not in user_stats:
        user_stats[user_id] = {
            "name": user_name,
            "username": user_username,
            "links_count": 0,
            "downloads_count": 0,
            "success_count": 0,
            "rank": "ئەندامێ چالاک"
        }

    stats = user_stats[user_id]
    
    # Calculate success rate safely
    total_l = stats['links_count']
    total_d = stats['downloads_count']
    success_rate = "100%" if total_d > 0 or total_l > 0 else "0%"

    profile_text = (
        f"╔═══════════════════════╗\n"
        f"     👤 **پروفایلا تەیێ تایبەت**     \n"
        f"╚═══════════════════════╝\n\n"
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
        f"💡 تێبینی: سیستەمێ تڕلیۆنی یێ بۆتی ب تەواوی زانیاریێن تە پارێزیت.\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    
    profile_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 نووکرنا پروفایلی", callback_data="my_profile"),
            InlineKeyboardButton("🔙 ڤەگەر", callback_data="back_home")
        ],
        [
            InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
        ]
    ])
    
    await callback_query.message.edit_text(profile_text, reply_markup=profile_kb)
    await callback_query.answer("✨ پروفایلا تە ب سەرکەفتن هاتە ڤەکرن!")

@app.on_callback_query(filters.regex(r"^my_downloads"))
async def downloads_callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    stats = user_stats.get(user_id, {"downloads_count": 0, "success_count": 0})
    
    dl_text = (
        f"📥 **بەشێ ڤیدیۆیێن داونلۆدكری:**\n\n"
        f"✨ هەتا نوکە تە ب دەستخستنا خۆ **{stats['downloads_count']}** فایل ب کوالیتیا بلندا 4K و MP3 دابەزاندینە.\n"
        f"🚀 کوالیتیا سیستەمی: 100% خێرا و بێ کێشە\n\n"
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
        f"📊 **ئامارێن گشتی یێن سیستەمی:**\n\n"
        f"👥 هژمارا کاربەرێن چالاک: {total_users}\n"
        f"📥 گشتی داونلۆدێن هاتیە کرن ل سیستەمی: {global_total_downloads}\n"
        f"⚡️ ڕەوشا سێرڤەری: 100% کارا و بێ کێشە\n\n"
        "👑 خودان: @YUSEEF_SURCHI"
    )
    
    stats_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")],
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    
    await callback_query.message.edit_text(stats_text, reply_markup=stats_kb)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^back_home"))
async def back_home_handler(client, callback_query: CallbackQuery):
    user_name = callback_query.from_user.first_name or "User"
    welcome_text = (
        f"🌟 سڵاو ل تە هەڤاڵێ خۆشەویست {user_name}!\n\n"
        "🔥🔥 ئەڤە هێزدارترین سیستەمێ داونلۆدکرنێ یێ بێ وێنە (تیکتۆک، اینستاگرام، و یوتیوب) ب کوالیتیا هەرە بلندا 4K و MP3 ب ناڤێ ڕاستەقینە!\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دەستپێکرنێ، لینکێ خۆ بۆ من بنێرە یان دوگمەیێن خوارێ بکاربينە!"
    )
    welcome_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 پروفایلا پێشکەفتى", callback_data="my_profile"),
            InlineKeyboardButton("📥 ڤیدیۆیێن داونلۆدکري", callback_data="my_downloads")
        ],
        [
            InlineKeyboardButton("📊 ئامارێن گشتی یێن بۆتی", callback_data="bot_global_stats")
        ],
        [
            InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")
        ]
    ])
    await callback_query.message.edit_text(welcome_text, reply_markup=welcome_kb)
    await callback_query.answer()

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def downloader_core_handler(client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"
    user_username = f"@{message.from_user.username}" if message.from_user.username else "نەدیار"
    url_link = message.text.strip()
    
    if user_id not in user_stats:
        user_stats[user_id] = {"name": user_name, "username": user_username, "links_count": 0, "downloads_count": 0, "success_count": 0, "rank": "ئەندامێ چالاک"}

    if not url_link.startswith("http") or not any(x in url_link.lower() for x in ["tiktok", "instagram", "insta.gram", "youtube", "youtu.be", "vm.tiktok"]):
        err_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
        ])
        await message.reply_text(
            "⚠️ برا، تنێ لینکێن **تیکتۆک، اینستاگرام، و یوتیوب** کار دکەن! هیڤیە لینکەکا دروست بۆ من بنێرە.\n\n"
            "👑 خودان: @YUSEEF_SURCHI",
            reply_markup=err_kb
        )
        return

    user_stats[user_id]["links_count"] += 1
    total_user_links = user_stats[user_id]["links_count"]

    process_msg = await message.reply_text(
        f"⚡️ سیستەمێ پێشکەفتى کار دکەت (کاربەر: {user_name} | لینکێن تە: {total_user_links}): نوکە زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n"
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

            await callback_query.message.reply_video(
                video=filename,
                caption="🎬 ب سەرکەفتن ڤیدیۆ (MP4) ب کوالیتیا بلند هاتە داونلۆدکرن!\n\n👑 خودان: @YUSEEF_SURCHI"
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
            await callback_query.message.reply_audio(
                audio=filename,
                title=audio_title,
                performer="YUSEEF_SURCHI",
                caption=f"🎶 سترانا تەمام ({audio_title}) ب کوالیتیا بلند و ب ناڤێ ڕاستەقینە هاتە داونلۆدکرن!\n\n👑 خودان: @YUSEEF_SURCHI"
            )

        if user_id in user_stats:
            user_stats[user_id]["downloads_count"] += 1
            user_stats[user_id]["success_count"] += 1
            # Auto update rank based on downloads
            if user_stats[user_id]["downloads_count"] >= 10:
                user_stats[user_id]["rank"] = "⭐ ئەندامێ پێشکەفتى"
            if user_stats[user_id]["downloads_count"] >= 50:
                user_stats[user_id]["rank"] = "🔥 ئەندامێ زێڕین"

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
        await status_msg.edit_text(f"❌ چەڵۆکیەک ڕوویدا د دەمێ داونلۆدکرنێ دا:\n`{str(e)}`\n\n👑 خودان: @YUSEEF_SURCHI")

print("🚀 Ultimate Supreme Advanced Profile Bot with Owner @YUSEEF_SURCHI is Running!")
app.run()
