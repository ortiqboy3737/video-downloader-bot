import asyncio
import os
import re
import shutil
import tempfile
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from yt_dlp import YoutubeDL

BOT_TOKEN = os.getenv("BOT_TOKEN")

URL_RE = re.compile(r"https?://\S+")

def extract_url(text):
    match = URL_RE.search(text)
    return match.group(0) if match else None

def download_video(url, workdir):
    ydl_opts = {
        "outtmpl": f"{workdir}/%(title)s.%(ext)s",
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "merge_output_format": "mp4",
        "quiet": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        return base + ".mp4"

async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    @dp.message(F.text == "/start")
    async def start(m: Message):
        await m.answer("YouTube / Instagram / TikTok link yuboring.")

    @dp.message(F.text)
    async def handle(m: Message):
        url = extract_url(m.text)
        if not url:
            await m.answer("Link yuboring.")
            return

        await m.answer("Yuklanmoqda...")

        workdir = tempfile.mkdtemp()

        try:
            filepath = await asyncio.to_thread(download_video, url, workdir)

            await m.answer_document(
                document=filepath,
                caption="Tayyor ✅"
            )

        except Exception as e:
            await m.answer(f"Xatolik: {e}")

        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
