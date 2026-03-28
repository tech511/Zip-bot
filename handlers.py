import os
import re
import time
import zipfile
import asyncio

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import app
from data import users_batch, batch_active, prefix_data, processing
from config import DOWNLOAD_DIR, ZIP_DIR
from helpers import extract_episode, glow_bar
from core.downloader import download_file
from core.queue import queue


# ============ LZIP COMMAND ============
@app.on_message(filters.command("lzip"))
async def lzip(client, message):

    uid = message.from_user.id

    # permission check (same as your logic)
    from data import admins
    from config import OWNER_ID

    if not (uid == OWNER_ID or uid in admins):
        return await message.reply_text("**🚫 You Are Not Authorized 😤**")

    if uid in processing:
        return await message.reply_text("⏳ Already in queue or processing")

    files = users_batch.get(uid)

    if not files:
        return await message.reply_text("No Files ❌")

    processing.add(uid)

    await queue.put((uid, message))

    await message.reply_text("✅ Added to Queue")


# ============ MAIN PROCESS ============
async def process_zip(uid, message):

    files = users_batch.get(uid)

    # extract name & quality (same as your code)
    match = re.findall(r"\[(.*?)\]", message.text or "")

    name = match[0] if len(match) > 0 else "Series"
    quality = match[-1] if len(match) > 1 else ""

    prefix = prefix_data.get(uid, "")

    msg = await message.reply_text("Starting...")

    start_time = time.time()
    done_size = 0

    # ===== PARALLEL DOWNLOAD =====
    tasks = []

    for i, m in enumerate(files):
        tasks.append(download_file(m, uid, i))

    paths = await asyncio.gather(*tasks)

    # ===== ZIP SYSTEM =====
    part = 1
    zip_path = f"{ZIP_DIR}/{uid}_part{part}.zip"
    z = zipfile.ZipFile(zip_path, "w")

    for i, file_path in enumerate(paths):

        size = os.path.getsize(file_path)
        done_size += size

        speed = done_size / (time.time() - start_time + 1) / (1024 * 1024)

        # split zip
        if os.path.exists(zip_path) and os.path.getsize(zip_path) > 1900 * 1024 * 1024:
            z.close()
            part += 1
            zip_path = f"{ZIP_DIR}/{uid}_part{part}.zip"
            z = zipfile.ZipFile(zip_path, "w")

        m = files[i]

        ep = extract_episode(m.caption or "") or f"E{i+1:02d}"

        new_name = f"{prefix} {name} {ep} {quality}.mkv"
        new_path = f"{DOWNLOAD_DIR}/{new_name}"

        os.rename(file_path, new_path)

        z.write(new_path, new_name)

        os.remove(new_path)

        # progress update (your style)
        await msg.edit_text(
            glow_bar(i + 1, len(files), speed, "📦 Processing"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
            ])
        )

    z.close()

    # ===== UPLOAD =====
    await msg.edit_text("📤 Uploading...")

    for f in os.listdir(ZIP_DIR):
        if f.startswith(str(uid)):
            path = os.path.join(ZIP_DIR, f)
            await message.reply_document(path)
            os.remove(path)

    # ===== CLEANUP =====
    for f in os.listdir(DOWNLOAD_DIR):
        os.remove(os.path.join(DOWNLOAD_DIR, f))

    users_batch[uid] = []
    batch_active.pop(uid, None)
    processing.discard(uid)


# ============ QUEUE WORKER LINK ============
from core.queue import worker

asyncio.get_event_loop().create_task(worker(process_zip))


# ============ REFRESH BUTTON ============
@app.on_callback_query(filters.regex("refresh"))
async def refresh(client, query):
    await query.answer("Updated")
