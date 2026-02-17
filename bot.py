import os
import yt_dlp
import asyncio
from pyrogram import Client, filters
from ai_engine import get_jarvis_response

# --- CONFIG ---
API_ID = 38318660
API_HASH = "af6449346924604501da5c1fae52b32d"
BOT_TOKEN = "8552567148:AAFX7Pv2X0U3kVoZ-Ks4zxCytv-1r_DKPKQ"
GEMINI_API_KEY = "AIzaSyCgio6zBbr8GHPmxu2aCeXSktgM-FF4HLw"

app = Client("Jarvis_Cloud", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.text & filters.private)
async def handle_all(client, message):
    if "http" not in message.text:
        # AI Answer
        reply = get_jarvis_response(message.text, GEMINI_API_KEY)
        await message.reply_text(reply)
    else:
        # Fast Downloader
        m = await message.reply_text("🚀 Downloading for you, Sir...")
        try:
            file_path = f"vid_{message.id}.mp4"
            opts = {'format': 'best', 'outtmpl': file_path, 'quiet': True}
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(opts).download([message.text]))
            await message.reply_document(file_path, caption="✅ Task Done, Amit Sir.")
            if os.path.exists(file_path):
                os.remove(file_path)
            await m.delete()
        except Exception as e:
            await m.edit(f"⚠️ Error: {str(e)[:50]}")

print("⚡ JARVIS IS READY FOR CLOUD ⚡")
app.run()
