from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# جایگزین کنید با توکن ربات خود
TOKEN = "7669113616:AAH6qqabVjqVu4X44GFrs68AjN3CaEFPoMg"
# شناسه یا نام کاربری کانال (مثال: "@YourChannelUsername" یا -1001234567890)
CHANNEL_ID = "Im_sadegh"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    فرمان /start برای خوش‌آمدگویی کاربر و توضیح عملکرد ربات
    """
    await update.message.reply_text(
        "سلام! این یک ربات پیام ناشناس است. هر پیامی که اینجا بفرستید به صورت ناشناس در کانال منتشر خواهد شد."
    )


async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    فرمان /setup برای ارسال یک پیام به کانال با دکمه شیشه‌ای که کاربر را به ربات هدایت می‌کند
    """
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username

    # ساخت دکمه شیشه‌ای با لینک به ربات
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ارسال پیام ناشناس",
                              url=f"https://t.me/{bot_username}")]
    ])

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="برای ارسال پیام ناشناس روی دکمه زیر کلیک کنید:",
        reply_markup=keyboard
    )
    await update.message.reply_text("🔧 تنظیمات کانال انجام شد.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    این هندلر تمام پیام‌های متنی خصوصی را دریافت کرده
    و بدون افشای هویت فرستنده به کانال ارسال می‌کند
    """
    if update.message.chat.type == "private":
        user_text = update.message.text
        # ارسال پیام به کانال به صورت ناشناس
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"📩 پیام ناشناس:\n{user_text}"
        )
        # اطلاع به فرستنده
        await update.message.reply_text("✅ پیام شما ارسال شد!")


def main() -> None:
    """
    نقطه ورود برنامه
    """
    app = ApplicationBuilder().token(TOKEN).build()

    # ثبت فرمان‌ها و هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setup", setup))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    # اجرای ربات
    app.run_polling()


if __name__ == "__main__":
    main()
