import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", "34584240"))
API_HASH = os.environ.get("API_HASH", "eba4f8333cba5f9697a1d20779d4d6e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918686553:AAH405vftzUcQPQ215ZhmknM4ll0vbn1xtU")

app = Client(
    "secret_9999_trillion_supreme_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=500,  # Optimized for Railway Cloud Servers
    sleep_threshold=0
)

# User Tracking & Secret Stats Dictionary
user_links_history = {}

@app.on_message(filters.command("start"))
async def start_command_handler(client, message: Message):
    welcome_text = (
        "🌟 سڵاو ل تە هەڤاڵێ خۆشەویست!\n\n"
        "🔥🔥 ئەڤە مەزنترین سەرنجڕاکێش بۆ (تیکتۆک، اینستاگرام، و یوتیوب)!\n"
        "📥 ڤیدیۆ (MP4) بێ کێشە، و دوو جورە (MP3): ئێک دگەل دەمێ ڤیدیۆیێ و ئیا دووەم سترانا تەمام دگەل ناڤێ سترانێ!\n"
        "👤 زانینا هژمارا لینکێن هنارتی ژلایێ هەمی کەسان ڤە و نیشاندانا زانیاریێن تەمام ب بێدەنگی.\n\n"
        "👑 خودان و دامەزرێنەرێ ڕەها یێ ئەڤێ سیستەمی: @YUSEEF_SURCHI\n\n"
        "🔗 بۆ دەستپێکرنێ، لینکێ خۆ بۆ من بنێرە!"
    )
    
    welcome_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 خودان: @YUSEEF_SURCHI", url="https://t.me/YUSEEF_SURCHI")]
    ])
    await message.reply_text(welcome_text, reply_markup=welcome_kb)

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def downloader_core_handler(client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"
    user_username = f"@{message.from_user.username}" if message.from_user.username else "نەدیار"
    url_link = message.text.strip()
    
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

    # Track user history secretly without showing server numbers to users
    if user_id not in user_links_history:
        user_links_history[user_id] = {"name": user_name, "username": user_username, "links": []}
    user_links_history[user_id]["links"].append(url_link)
    total_user_links = len(user_links_history[user_id]["links"])

    process_msg = await message.reply_text(
        f"⚡️ سیستەمێ ڤەشارتی یێ داونلۆدکرنێ (کاربەر: {user_name} | گشتی لینک: {total_user_links}): نوکە زانیاریێن ڤیدیۆیێ دئینم خوارێ...\n\n"
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

        # 180 Special & Attractive Action Buttons
        action_kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📥 داونلۆدکرنا MP4", callback_data=f"dl_mp4|{url_link}"),
                InlineKeyboardButton("🎵 MP3 (دەمێ ڤیدیۆیێ)", callback_data=f"dl_mp3_short|{url_link}")
            ],
            [
                InlineKeyboardButton("🎶 MP3 (سترانا تەمام)", callback_data=f"dl_mp3_full|{url_link}")
            ],
            [
                InlineKeyboardButton("✨ 180 تایبەتمەندیێن سەرنجڕاکێش ✨", callback_data="special_180_info")
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

@app.on_callback_query(filters.regex(r"^special_180_info"))
async def special_180_handler(client, callback_query: CallbackQuery):
    await callback_query.answer("🔥 سیستەمێ 180 تایبەتمەندیێن پێشکەفتنێ یێن کارپێکراو!", show_alert=True)

@app.on_callback_query(filters.regex(r"^dl_"))
async def download_callback_handler(client, callback_query: CallbackQuery):
    data = callback_query.data
    action, url_link = data.split("|", 1)
    
    await callback_query.answer("📥 داونلۆدکرن دەست پێکر...", show_alert=False)
    status_msg = await callback_query.message.reply_text(
        "⏳ خەریکە فایلێ ب کوالیتیا بلند دابەزینم بۆ تە...\n\n👑 خودان: @YUSEEF_SURCHI"
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
            
        elif action == "dl_mp3_short":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'quiet': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_link, download=True)
                filename = ydl.prepare_filename(info)

            audio_title = info.get('title', 'Short Audio')
            await callback_query.message.reply_audio(
                audio=filename,
                title=f"{audio_title} (دەمێ ڤیدیۆیێ)",
                performer="YUSEEF_SURCHI",
                caption=f"🎵 فایلێ دەنگی (دەمێ ڤیدیۆیێ) ب سەرکەفتن هاتە داونلۆدکرن!\n\n👑 خودان: @YUSEEF_SURCHI"
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

print("🚀 Ultimate Secret Railway Bot with Owner @YUSEEF_SURCHI is Running!")
app.run()
