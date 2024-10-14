import time
import json
import telebot
import random

## TOKEN DETAILS
TOKEN = "TON"  # يجب استبدال هذا بالتوكن الصحيح
BOT_TOKEN = "8148048276:AAG7Bw7OHeru80X_Fa_x-vHiI61WaxrX4jM"
PAYMENT_CHANNEL = "@tastttast"  # إضافة القناة هنا بما في ذلك علامة '@'
OWNER_ID = 1002163515274  # أدخل معرف المشرف هنا
CHANNELS = ["@tastttast"]  # إضافة القنوات التي سيتم التحقق منها هنا
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/c/YourChannelName"  # استبدل هذا برابط قناتك
Daily_bonus = 2  # مقدار الهدية اليومية
Mini_Withdraw = 1000  # الحد الأدنى للسحب
Per_Refer = 3  # مكافأة الإحالة

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for channel in CHANNELS:
        check = bot.get_chat_member(channel, id)
        if check.status == 'left':
            return False
    return True

def menu(user_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '🎁 Bonus', '💸 Withdraw')
    keyboard.row('⚙️ Set Wallet', '📊 Statistics', '🎮 Play Games')  # إضافة زر الألعاب
    bot.send_message(user_id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    # نفس كود البدء الموجود سابقا
    ...

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    # نفس كود استجابة الاستعلام الموجود سابقا
    ...

@bot.message_handler(content_types=['text'])
def send_text(message):
    user_id = str(message.chat.id)
    try:
        data = json.load(open('users.json', 'r'))

        if message.text == '🎮 Play Games':
            games_menu(user_id)

        elif message.text == '🆔 Account':
            # الكود السابق
            ...

        # باقي كود معالجة الرسائل الموجود سابقا
        ...

    except Exception as e:
        bot.send_message(message.chat.id, "هذا الأمر به خطأ، يرجى الانتظار حتى يتم إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

def games_menu(user_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🎲 لعبة الرقم العشوائي')
    keyboard.row('🔙 العودة إلى الرئيسية')
    bot.send_message(user_id, "اختر لعبة للعب:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == '🎲 لعبة الرقم العشوائي')
def random_game(message):
    user_id = str(message.chat.id)
    winning_number = random.randint(1, 10)  # الرقم الفائز
    bot.send_message(user_id, "تخمين رقم بين 1 و 10:")

    bot.register_next_step_handler(message, check_guess, winning_number)

def check_guess(message, winning_number):
    user_id = str(message.chat.id)
    guess = int(message.text)

    if guess == winning_number:
        bot.send_message(user_id, "🎉 لقد ربحت! حصلت على 5 نقاط إضافية.")
        update_balance(user_id, 5)  # تحديث الرصيد
    else:
        bot.send_message(user_id, f"❌ خاب أملك! الرقم الصحيح هو {winning_number}.")

def update_balance(user_id, points):
    data = json.load(open('users.json', 'r'))
    if user_id in data['balance']:
        data['balance'][user_id] += points
    else:
        data['balance'][user_id] = points
    json.dump(data, open('users.json', 'w'))

# الدالة set_wallet و bot.polling تظل كما هي

bot.polling(none_stop=True)
