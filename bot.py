import asyncio, json, os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import check_new_pins
from store import save_user_cookie, save_target_user, get_user_data

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "PASTE_YOUR_BOT_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Pinterest Spy Bot!\nSend /setcookie <your _pinterest_sess cookie>")

async def setcookie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /setcookie _pinterest_sess=...")
    cookie = " ".join(context.args)
    save_user_cookie(update.effective_user.id, cookie)
    await update.message.reply_text("✅ Cookie saved. Now send /setuser <username>")

async def setuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /setuser username")
    username = context.args[0]
    save_target_user(update.effective_user.id, username)
    await update.message.reply_text(f"✅ Now tracking public saved pins of {username} every 60 sec.")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await check_new_pins(update.effective_user.id)
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setcookie", setcookie))
app.add_handler(CommandHandler("setuser", setuser))
app.add_handler(CommandHandler("check", check))

async def background_loop():
    while True:
        with open("users.json", "r") as f:
            users = json.load(f)
        for uid in users:
            try:
                msg = await check_new_pins(int(uid))
                if msg != "No new pins found.":
                    await app.bot.send_message(chat_id=uid, text=msg)
            except Exception as e:
                print(f"[!] Error for {uid}: {e}")
        await asyncio.sleep(60)

async def main():
    await app.initialize()
    await app.start()
    asyncio.create_task(background_loop())
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
