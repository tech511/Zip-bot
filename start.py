from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import app
from data import start_image

@app.on_message(filters.command("start"))
async def start(client, message):

    text = f"""**╔═══『 🤖 ZIP BOT 』═══╗**

**👋 Hello, {message.from_user.first_name}**

__I Can Convert Files Into Zip Easily.__

***⚡ Fast • Smart • Reliable ⚡***

> **Maintain By:** @AniWorld_Bot_Hub

**╚═══════════════════════╝**"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/AniWorld_Bot_Hub"),
            InlineKeyboardButton("📜 Commands", callback_data="cmd")
        ],
        [
            InlineKeyboardButton("📢 Update", url="https://t.me/AniWorld_Bot_Hub")
        ]
    ])

    if start_image:
        await message.reply_photo(start_image, caption=text, reply_markup=buttons)
    else:
        await message.reply_text(text, reply_markup=buttons)
