import logging from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters from dotenv import load_dotenv import os
# Load environment variables load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Check if BOT_TOKEN is loaded correctly if not BOT_TOKEN: raise ValueError("Bot token not found in environment variables.")
# Enable logging with the correct format logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__) user_data = {}
# Define plan prices and details plan_prices = {
'monthly_15gb': '١۵٠ ھزار تومان',
'monthly_50gb': '٣۵٠ ھزار تومان',
'monthly_100gb': '۶٠٠ ھزار تومان',
'yearly_600gb': '١/٣٨٠/٠٠٠ تومان',
'yearly_1200gb': '١/٩٢٠/٠٠٠ تومان',
'yearly_3600gb': '٣/۵۴٠/٠٠٠ تومان'
}
plan_details = {
'monthly_15gb': { 'price': '١۵٠ ھزار تومان',
'bank_link': 'https://zarinp.al/610691',
'crypto_price': '2.6 تتر',
'crypto_wallet': '0xb646C62b0096f31572b9cbA623188000adE36201'
},
'monthly_50gb': { 'price': '٣۵٠ ھزار تومان',
'bank_link': 'https://zarinp.al/610692',
'crypto_price': '6.1 تتر',
'crypto_wallet': '0xb646C62b0096f31572b9cbA623188000adE36201'
},
'monthly_100gb': { 'price': '۶٠٠ ھزار تومان',
'bank_link': 'https://zarinp.al/610693',
'crypto_price': '10.4 تتر',
'crypto_wallet': '0xb646C62b0096f31572b9cbA623188000adE36201'
},
'yearly_600gb': {
'price': '١/٣٨٠/٠٠٠ تومان',
'bank_link': 'https://zarinp.al/610695',
'crypto_price': '23.8 تتر',
'crypto_wallet': '0xb646C62b0096f31572b9cbA623188000adE36201'
},
'yearly_1200gb': {
'price': '١/٩٢٠/٠٠٠ تومان',
'bank_link': 'https://zarinp.al/610697',
'crypto_price': '33.2 تتر',
'crypto_wallet': '0xb646C62b0096f31572b9cbA623188000adE36201'
},
'yearly_3600gb': {
'price': '٣/۵۴٠/٠٠٠ تومان',
'bank_link': 'https://zarinp.al/610698',
'crypto_price': '61 تتر',
'crypto_wallet': '0xb646C62b0096f31572b9cbA623188000adE36201'
}
}
# Start command handler async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
user_id = update.message.from_user.id keyboard = [
[
InlineKeyboardButton("🔄 خرید اکانت جدید", callback_data='buy_account'),
InlineKeyboardButton("📋 فھرست اکانت ھا", callback_data='list_accounts')
],
[
InlineKeyboardButton("📣 کانال تلگرام", url='https://t.me/CEEPORTVPNCHANNEL')
],
[
InlineKeyboardButton("ℹ درباره ربات", callback_data='about_bot')
]
]
if user_id in user_data and user_data[user_id].get('confirmed'):
keyboard.insert(1, [InlineKeyboardButton("💳 وضعیت پرداخت",
callback_data='payment_status')]) else: keyboard.insert(1, [InlineKeyboardButton("💳 پرداخت", callback_data='payment')])
reply_markup = InlineKeyboardMarkup(keyboard) await update.message.reply_text(' بھ رباتCeeportVPN خوش آمدید!\nلطفاً یک گزینھ را انتخاب کنید:',
reply_markup=reply_markup)
# Callback query handler async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
query = update.callback_query user_id = query.from_user.id await query.answer()
logger.info(f"Callback query data: {query.data}") logger.info(f"User data before processing: {user_data.get(user_id, {})}")
if query.data == 'start':
keyboard = [
[
InlineKeyboardButton("🔄 خرید اکانت جدید", callback_data='buy_account'),
InlineKeyboardButton("📋 فھرست اکانت ھا", callback_data='list_accounts')
],
[
InlineKeyboardButton("📣 کانال تلگرام", url='https://t.me/CEEPORTVPNCHANNEL')
],
[
InlineKeyboardButton("ℹ درباره ربات", callback_data='about_bot')
]
]
if user_id in user_data and user_data[user_id].get('confirmed'):
keyboard.insert(1, [InlineKeyboardButton("💳 وضعیت پرداخت",
callback_data='payment_status')]) else: keyboard.insert(1, [InlineKeyboardButton("💳 پرداخت", callback_data='payment')])
reply_markup = InlineKeyboardMarkup(keyboard) await query.edit_message_text(' بھ رباتCeeportVPN خوش آمدید!\nلطفاً یک گزینھ را انتخاب کنید:', reply_markup=reply_markup)
elif query.data == 'buy_account': await query.edit_message_text(
text=" لطفاً پروتکل سرورVPN خود را انتخاب کنید:", reply_markup=InlineKeyboardMarkup([
[InlineKeyboardButton("🛡 Outline", callback_data='outline')],
[InlineKeyboardButton("🔙 برگشت", callback_data='start')]
])
)
elif query.data == 'outline':
keyboard = [
[InlineKeyboardButton("🔒 TCP", callback_data='outline_tcp')],
[InlineKeyboardButton("🌐 UDP", callback_data='outline_udp')],
[InlineKeyboardButton("🔙 برگشت", callback_data='buy_account')],
[InlineKeyboardButton("🏠 خانھ", callback_data='start')]
]
await query.edit_message_text(
text=" نوع پورتVPN Outline را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard)
)
elif query.data == 'outline_tcp' or query.data == 'outline_udp': user_data[user_id] = {'protocol': query.data.split('_')[1]} countries = [
("کانادا", "\U0001F1E8\U0001F1E6"), ("انگلستان", "\U0001F1EC\U0001F1E7"), ("استونی",
"\U0001F1EA\U0001F1EA"),
("فنلاند", "\U0001F1EB\U0001F1EE"), ("فرانسھ", "\U0001F1EB\U0001F1F7"), ("آلمان",
"\U0001F1E9\U0001F1EA"),
("لیتوانی", "\U0001F1F1\U0001F1F9"), ("ھلند", "\U0001F1F3\U0001F1F1"), ("لھستان",
"\U0001F1F5\U0001F1F1"),
("روسیھ", "\U0001F1F7\U0001F1FA"), ("سوئد", "\U0001F1F8\U0001F1EA"), ("ترکیھ",
"\U0001F1F9\U0001F1F7"),
("اوکراین", "\U0001F1FA\U0001F1E6"), ("ایالات متحده آمریکا", "\U0001F1FA\U0001F1F8")
]
keyboard = [[InlineKeyboardButton(f"{flag} {country}", callback_data=f'country_{country}')
for country, flag in countries[i:i+2]] for i in range(0, len(countries), 2)] keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data='outline')]) keyboard.append([InlineKeyboardButton("🏠 خانھ", callback_data='start')]) await query.edit_message_text(
,":لطفاً مکان ( کشور ) ارائھ دھنده سرور خود را انتخاب کنیدtext="reply_markup=InlineKeyboardMarkup(keyboard)
) elif query.data.startswith('country_'): user_data[user_id]['country'] = query.data.split('_')[1] await query.edit_message_text(
,":بازه زمانی مورد نیاز برای اکانت خود را انتخاب کنیدtext="reply_markup=InlineKeyboardMarkup([
[InlineKeyboardButton("📅  ماھانھ ( محاسبھ با تخفیف)", callback_data='monthly')],
[InlineKeyboardButton("📆  سالانھ ( محاسبھ با تخفیف)", callback_data='yearly')],
[InlineKeyboardButton("🔙 برگشت", callback_data=f'outline_{user_data[user_id]["protocol"]}')],
[InlineKeyboardButton("🏠 خانھ", callback_data='start')]
])
)
elif query.data == 'monthly' or query.data == 'yearly':
user_data[user_id]['duration'] = query.data keyboard = [] if query.data == 'monthly':
keyboard = [
[InlineKeyboardButton(f"💾 ١۵  گیگابایت= {plan_prices['monthly_15gb']}", callback_data='monthly_15gb')],
[InlineKeyboardButton(f"💾 ۵٠  گیگابایت= {plan_prices['monthly_50gb']}", callback_data='monthly_50gb')],
[InlineKeyboardButton(f"💾 ١٠٠  گیگابایت= {plan_prices['monthly_100gb']}",
callback_data='monthly_100gb')]
]
elif query.data == 'yearly':
keyboard = [
[InlineKeyboardButton(f"💾 ۶٠٠  گیگابایت= {plan_prices['yearly_600gb']}", callback_data='yearly_600gb')],
[InlineKeyboardButton(f"💾 ١٢٠٠  گیگابایت= {plan_prices['yearly_1200gb']}", callback_data='yearly_1200gb')],
[InlineKeyboardButton(f"💾 ٣۶٠٠  گیگابایت= {plan_prices['yearly_3600gb']}",
callback_data='yearly_3600gb')]
]
keyboard.append([InlineKeyboardButton("🔙 برگشت",
callback_data=f'country_{user_data[user_id]["country"]}')]) keyboard.append([InlineKeyboardButton("🏠 خانھ", callback_data='start')])
await query.edit_message_text(
text=f"30}  بستھ حجمی پلنif query.data == 'monthly' else 365}  روزهOutline را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard)
)
elif query.data.endswith('15gb') or query.data.endswith('50gb') or query.data.endswith('100gb')
or query.data.endswith('600gb') or query.data.endswith('1200gb') or query.data.endswith('3600gb'):
user_data[user_id]['plan'] = query.data plan_price = plan_prices[query.data] keyboard = [
[InlineKeyboardButton("💳 پرداخت بانکی", callback_data='bank_payment')],
[InlineKeyboardButton("🏦 پرداخت با ارز دیجیتال", callback_data='crypto_payment')],
[InlineKeyboardButton("🔙 برگشت", callback_data=user_data[user_id]['duration'])], [InlineKeyboardButton("🏠 خانھ", callback_data='start')]
]
await query.edit_message_text(نرخ پلن بستھ بھ نرخ دلار متغیر است و احتمال کاھش:\n\nلطفاً یکی از روش ھای پرداخت زیر را انتخاب کنیدtext=f"{plan_price}**", :پلن انتخابی شما.\n\n**و افزایش وجود خواھد داشتparse_mode="Markdown",reply_markup=InlineKeyboardMarkup(keyboard)
)
elif query.data == 'bank_payment' or query.data == 'crypto_payment':
user_data[user_id]['payment_method'] = query.data selected_plan = user_data[user_id]['plan'] plan_price = plan_details[selected_plan]['price'] payment_text = (
f"شناسھ کاربری: {user_id}\n" f"پروتکل: {user_data[user_id]['protocol']}\n" f"کشور: {user_data[user_id]['country']}\n" f"بازه زمانی: {user_data[user_id]['duration']}\n" f"حجم: {selected_plan}\n" f"روش پرداخت: {'بانکی' if query.data == 'bank_payment' else 'ارز دیجیتال'}\n" f"مبلغ: {plan_price}\n"
)
if query.data == 'bank_payment':
payment_text += f"لینک پرداخت: {plan_details[selected_plan]['bank_link']}\n"
else: payment_text += f"مبلغ بھ تتر: {plan_details[selected_plan]['crypto_price']}\n"
keyboard = [
[InlineKeyboardButton("✅ تایید فاکتور", callback_data='confirm_invoice')],
[InlineKeyboardButton("🔄 تغییر پلن", callback_data='change_plan')],
[InlineKeyboardButton("❌ حذف فاکتور", callback_data='delete_invoice')],
[InlineKeyboardButton("🔙 برگشت", callback_data=user_data[user_id]['plan'])], [InlineKeyboardButton("🏠 خانھ", callback_data='start')]
]
# Save the pre-invoice separately user_data[user_id]['pre_invoice'] = payment_text
await query.edit_message_text( text=f"فاکتور شما:\n{payment_text}\n"
,".لطفاً مبلغ را پرداخت کنید و تصویر تراکنش را ھمراه با فاکتور بھ آیدی پشتیبان ارسال کنیدf"reply_markup=InlineKeyboardMarkup(keyboard)
)
elif query.data == 'confirm_invoice':
user_data[user_id]['confirmed'] = True selected_plan = user_data[user_id]['plan'] plan_price = plan_details[selected_plan]['price'] account_id =
f"{user_id}_{selected_plan}_{user_data[user_id]['protocol']}_{user_data[user_id]['country']}"
if 'accounts' not in user_data[user_id]:
user_data[user_id]['accounts'] = []
user_data[user_id]['accounts'].append(account_id) final_payment_text = user_data[user_id]['pre_invoice'] + f"\nشناسھ اکانت: {account_id}\n"
# Save the final invoice separately user_data[user_id]['final_invoice'] = final_payment_text
keyboard = [
[InlineKeyboardButton("🔄 تغییر پلن", callback_data='change_plan')],
[InlineKeyboardButton("❌ حذف فاکتور", callback_data='delete_invoice')],
[InlineKeyboardButton("🔙 برگشت", callback_data='start')]
]
await query.edit_message_text( text=f"✅ فاکتور شما تایید شد:\n{final_payment_text}\n"
,".لطفاً مبلغ را پرداخت کنید و تصویر تراکنش را ھمراه با فاکتور بھ آیدی پشتیبان ارسال کنیدf"reply_markup=InlineKeyboardMarkup(keyboard)
)
await context.bot.send_message( chat_id=user_id, text=f"✅ فاکتور شما تایید شد:\n{final_payment_text}\n"
".لطفاً مبلغ را پرداخت کنید و تصویر تراکنش را ھمراه با فاکتور بھ آیدی پشتیبان ارسال کنیدf"
)
if user_data[user_id]['payment_method'] == 'crypto_payment':
await context.bot.send_message( chat_id=user_id,
":آدرس ولت برای پرداختtext="
)
await context.bot.send_message( chat_id=user_id, text=f"{plan_details[selected_plan]['crypto_wallet']}"
)
elif query.data == 'payment_status':
if user_id in user_data and user_data[user_id].get('final_invoice'):
final_payment_text = user_data[user_id]['final_invoice'] keyboard = [
[InlineKeyboardButton("🔄 تغییر پلن", callback_data='change_plan')],
[InlineKeyboardButton("❌ حذف فاکتور", callback_data='delete_invoice')],
[InlineKeyboardButton("🔙 برگشت", callback_data='start')]
]
await query.edit_message_text( text=f"✅ فاکتور شما تایید شد:\n{final_payment_text}\n"
,".لطفاً مبلغ را پرداخت کنید و تصویر تراکنش را ھمراه با فاکتور بھ آیدی پشتیبان ارسال کنیدf"reply_markup=InlineKeyboardMarkup(keyboard)
)
else:
await query.edit_message_text(
,".شما ھیچ فاکتور تایید شده ای نداریدtext="
reply_markup=InlineKeyboardMarkup([
[InlineKeyboardButton("🔙 برگشت", callback_data='start')]
])
)
elif query.data == 'change_plan': user_data.pop(user_id, None) await query.edit_message_text(
,".پلن شما حذف شد. لطفاً یک پلن جدید انتخاب کنیدtext="reply_markup=InlineKeyboardMarkup([
[InlineKeyboardButton("🔄 خرید اکانت جدید", callback_data='buy_account')],
[InlineKeyboardButton("📋 فھرست اکانت ھا", callback_data='list_accounts')],
[InlineKeyboardButton("📣 کانال تلگرام", url='https://t.me/CEEPORTVPNCHANNEL')],
[InlineKeyboardButton("💳 پرداخت", callback_data='payment')],
[InlineKeyboardButton("ℹ درباره ربات", callback_data='about_bot')],
[InlineKeyboardButton("🏠 خانھ", callback_data='start')]
])
)
elif query.data == 'delete_invoice': user_data.pop(user_id, None) await query.edit_message_text(
,".فاکتور شما حذف شد. لطفاً یک پلن جدید انتخاب کنیدtext="reply_markup=InlineKeyboardMarkup([
[InlineKeyboardButton("🔄 خرید اکانت جدید", callback_data='buy_account')],
[InlineKeyboardButton("📋 فھرست اکانت ھا", callback_data='list_accounts')],
[InlineKeyboardButton("📣 کانال تلگرام", url='https://t.me/CEEPORTVPNCHANNEL')],
[InlineKeyboardButton("💳 پرداخت", callback_data='payment')],
[InlineKeyboardButton("ℹ درباره ربات", callback_data='about_bot')],
[InlineKeyboardButton("🏠 خانھ", callback_data='start')]
])
)
elif query.data == 'list_accounts':
if user_id in user_data and 'accounts' in user_data[user_id]: accounts_text = "\n".join(user_data[user_id]['accounts']) await query.edit_message_text( text=f"شناسھ اکانت ھای شما:\n{accounts_text}", reply_markup=InlineKeyboardMarkup([
[InlineKeyboardButton("🔙 برگشت", callback_data='start')]
])
)
else:
await query.edit_message_text(
text="شما ھیچ اکانت خریداری شده ای ندارید.", reply_markup=InlineKeyboardMarkup([
[InlineKeyboardButton("🔙 برگشت", callback_data='start')]
])
)
elif query.data == 'about_bot':
about_text = """
😊 !برای رفع محدودیت ھا در کنار حفظ امنیت و حریم خصوصی شماVPN  بھترین😉 
🌟 !سلام دوستانما، م یتوانید ازVPN  مطمئن و پرسرعت ھستید؟🚀  ما بھترین پیشنھاد را برای شما داریم! با استفاده ازVPN  آیا بھ دنبال یک
:مزایای بی شماری بھره مند شوید
.امنیت بالا: اطلاعات شما در برابر ھکرھا و جاسوسان محافظت می شود ✅
.حفظ حریم خصوصی: بدون نگرانی از ردیابی، بھ صورت ناشناس در اینترنت گشت و گذار کنید ✅
.دسترسی بھ محتوای مسدود شده: بھ راحتی بھ سایت ھا و خدمات محدود شده دسترسی پیدا کنید ✅
.سرعت بالا و پایداری: تجربھ بی نظیری از اینترنت پرسرعت داشتھ باشید ✅
امکان پرداخت از طریق درگاه امن بانکی ✅USDT-BEP20. :امکان پرداخت با ارز دیجیتال ✅قابل اجرا در ایفون و اندروید ✅
🔖 پشتبانی ۴٢ ساعتھقابل اتصال با تمام اپراتورھای ارائھ دھنده اینترنت🌀 عملکرد عالی برای عبور از شدیدترین تحریم ھا🌀 
ترافیک انتخابی🌀 مدت اشتراک ماھانھ و سالانھ🌀 دارای لوکیشن ھای مختلف و آی پی ثابت🌀 کیفیت و سرعت دانلود و آپلود فضایی🌀 دارای ضمانت و پشتیبانی تا لحظھ آخر اشتراک🌀 اختصاصی برای ھر استفاده کننده🌀 قیمت کمتر بھ نسبت سایر سرویس ھا🌀 
:پیشنھاد ویژه💥 
!ھمین حالا بھ جمع مشتریان راضی ما بپیوندید و از تخفیف ویژه برای اولین خرید خود بھره مند شوید
.🌍🔐 !حریم خصوصی و امنیت شما اولویت ماست
"""
keyboard = [
[InlineKeyboardButton("🔙 برگشت", callback_data='start')]
]
await query.edit_message_text(text=about_text,
reply_markup=InlineKeyboardMarkup(keyboard))
# Handle payment receipt async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
user_id = update.message.from_user.id if user_id in user_data and user_data[user_id].get('confirmed'): user_data[user_id]['receipt'] = update.message.photo[-1].file_id
(".فیش پرداختی دریافت شد. پس از بررسی، اکانت شما فعال خواھد شدawait update.message.reply_text("else:
(".شما فاکتور تایید شده ای ندارید. لطفاً ابتدا فاکتور را تایید کنیدawait update.message.reply_text("
# Error handler async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
"""Log the error and send a telegram message to notify the developer.""" logger.error(msg="Exception while handling an update:", exc_info=context.error) await context.bot.send_message(chat_id='YOUR_CHAT_ID', text=str(context.error))
# Main function to start the bot def main() -> None:
application = ApplicationBuilder().token(BOT_TOKEN).build() application.add_handler(CommandHandler("start", start)) application.add_handler(CallbackQueryHandler(button)) application.add_handler(MessageHandler(filters.PHOTO, handle_receipt))
# Add the error handler
application.add_error_handler(error_handler)
# Start the Bot
application.run_polling()
if __name__ == '__main__':
main()
