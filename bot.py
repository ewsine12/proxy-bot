import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, PROXY_API_KEY, ADMIN_ID, API_URL
from utils import is_admin, add_user, update_gb, set_country, get_gb
from country_codes import get_code

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌍 Change Country", callback_data='country')],
        [InlineKeyboardButton("📊 Check GB", callback_data='check_gb')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🚀 Welcome! Choose an option:", reply_markup=reply_markup)

# Button callback
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "country":
        await query.edit_message_text("🌍 Send /country <Country Code or Full Name>")
    elif query.data == "check_gb":
        user = get_gb(query.from_user.id)
        if user:
            allocated, used = user
            await query.edit_message_text(f"📊 GB Used: {used} / {allocated}")
        else:
            await query.edit_message_text("❌ You have no proxy package")

# Admin: create package
async def create_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id, ADMIN_ID):
        return await update.message.reply_text("❌ Admin only command")
    try:
        telegram_id = int(context.args[0])
        gb = float(context.args[1].replace("GB",""))
        payload = {"api_key": PROXY_API_KEY, "traffic_limit": gb}
        r = requests.post(f"{API_URL}/residentsubuser/create", json=payload)
        data = r.json()
        add_user(telegram_id, data["subuser_id"], data["package_key"], gb)
        await update.message.reply_text(f"✅ User Created with {gb}GB")
    except:
        await update.message.reply_text("Usage: /create_user TELEGRAM_ID 5GB")

# User: country change
async def country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("Usage: /country US or /country United States")
    name = " ".join(context.args)
    code, full = get_code(name)
    if not code:
        return await update.message.reply_text("❌ Invalid country")
    set_country(update.effective_user.id, code, full)
    payload = {"api_key": PROXY_API_KEY, "country": code}
    requests.post(f"{API_URL}/residentsubuser/list/update", json=payload)
    await update.message.reply_text(f"🌍 Country changed to {full} ({code})")

# User: check GB
async def mygb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_gb(update.effective_user.id)
    if user:
        allocated, used = user
        await update.message.reply_text(f"📊 GB Used: {used} / {allocated}")
    else:
        await update.message.reply_text("❌ You have no proxy package")

# Bot setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CommandHandler("create_user", create_user))
app.add_handler(CommandHandler("mygb", mygb))
app.add_handler(CommandHandler("country", country))
app.run_polling()
