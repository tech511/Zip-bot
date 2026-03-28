from pyrogram import Client
from config import *

import os

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(ZIP_DIR, exist_ok=True)

app = Client(
    "final_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=10
)

# Import all handlers
import handlers.start
import handlers.admin
import handlers.prefix
import handlers.batch
import handlers.lzip

print("Bot Running...")
app.run()
