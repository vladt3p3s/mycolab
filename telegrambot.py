from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import re

TOKEN = "7571143442:AAH64EjjOQFmvgWSyhMrT47iKAlim9tC_7k"

LINK_PATTERN = re.compile(
    r"(?i)"  
    r"(?:"
    r"(?:(?:https?|ftp):\/\/|www\.)" 
    r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"  
    r"(?::\d{1,5})?"  
    r"(?:\/[^\s#]*)?(?:#[^\s]*)?"  
    r"|"
    r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d{1,5})?(?:\/[^\s#]*)?(?:#[^\s]*)?"  
    r"|"
    r"(?:\d{1,3}\.){3}\d{1,3}(?::\d{1,5})?(?:\/[^\s#]*)?(?:#[^\s]*)?" 
    r"|"
    r"(?:https?:\/\/|www\.)?t\.me\/(?:s\/)?(?:\+?[a-zA-Z0-9_-]+|joinchat\/[a-zA-Z0-9_-]+)"  
    r"|"
    r"(?:https?:\/\/|www\.)?(?:bit\.ly|t\.co|tinyurl\.com|goo\.gl|is\.gd|buff\.ly|shrtco\.de|cutt\.ly|"
    r"rebrand\.ly|ow\.ly|bit\.do|t2m\.io|mcaf\.ee|qr\.ae|v\.gd|rb\.gy|lnk\.to|shorturl\.at|t\.ly|"
    r"gg\.gg|u\.nu|clck\.ru)\/[a-zA-Z0-9_-]+" 
    r")"
)



async def ban(update: Update, context):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await update.effective_chat.ban_member(user_id)
        await update.message.reply_text(f"User {user_id} banned by a moderator.")

async def unban(update: Update, context):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await update.effective_chat.unban_member(user_id)
        await update.message.reply_text(f"User {user_id} is no longer banned.")

async def detect_and_ban(update: Update, context):
    text = update.message.text
    user_id = update.message.from_user.id

    if LINK_PATTERN.search(text):
        await update.message.delete()
        await update.effective_chat.ban_member(user_id)
        await update.message.reply_text(f"Links are not allowed in channel. User: {user_id} is banned.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_and_ban))

    app.run_polling()

if __name__ == "__main__":
    main()