from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات
TOKEN = "7669113616:AAH6qqabVjqVu4X44GFrs68AjN3CaEFPoMg"

# شناسه کانال (به‌صورت @channel_username)
CHANNEL_ID = "@im_sadegh"

# آیدی عددی ادمین (برای دریافت پیام‌های ناشناس)
ADMIN_CHAT_ID = 5280481527


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "سلام! اینجا پیام شما به صورت ناشناس برای ادمین ارسال خواهد شد."
    )


async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    ارسال پیام حاوی دکمه شیشه‌ای به کانال برای دریافت پیام ناشناس
    """

    # گرفتن یوزرنیم ربات برای ساختن لینک به خودش
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ارسال پیام ناشناس",
                               url=f"https://t.me/{bot_username}")]]
    )

    try:
        # ارسال پیام به کانال
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="برای ارسال پیام ناشناس روی دکمه زیر کلیک کنید:",
            reply_markup=keyboard
        )
        await update.message.reply_text("✅ پیام دارای دکمه به کانال ارسال شد.")
    except Exception as e:
        await update.message.reply_text(f"❌ خطا در ارسال به کانال: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    دریافت پیام خصوصی و ارسال آن برای ادمین به‌صورت ناشناس
    """
    if update.message.chat.type == "private":
        user = update.message.from_user
        msg = update.message.text

        # متن ارسالی به ادمین
        report = (
            "📥 پیام ناشناس جدید:\n"
            f"👤 نام: {user.full_name}\n"
            f"🔗 یوزرنیم: @{user.username or 'ندارد'}\n"
            f"🆔 آیدی: {user.id}\n"
            f"📝 متن:\n{msg}"
        )

        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=report)
        await update.message.reply_text("✅ پیام شما به ادمین ارسال شد.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setup", setup))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
