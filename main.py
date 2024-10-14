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
    keyboard.row('⚙️ Set Wallet', '📊 Statistics')  # الإحصائيات للمشرف فقط
    keyboard.row('🎮 Play Games')  # إضافة خيار الألعاب
    bot.send_message(user_id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    try:
        data = json.load(open('users.json', 'r'))

        if user_id not in data['referred']:
            data['referred'][user_id] = 0
            data['total'] += 1
        if user_id not in data['referby']:
            data['referby'][user_id] = user_id
        if user_id not in data['checkin']:
            data['checkin'][user_id] = 0
        if user_id not in data['balance']:
            data['balance'][user_id] = 0
        if user_id not in data['wallet']:
            data['wallet'][user_id] = "none"
        json.dump(data, open('users.json', 'w'))

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
        msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n"
        for channel in CHANNELS:
            msg_start += f"➡️ {channel}\n"
        msg_start += f"➡️ و يجب عليك الاشتراك في قناتي على اليوتيوب:\n{YOUTUBE_CHANNEL_URL}\n"
        msg_start += "*"
        bot.send_message(user_id, msg_start, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, "حدث خطأ، يرجى الانتظار حتى يتم إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                bot.answer_callback_query(call.id, text='✅ You joined, Now you can earn money')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user_id not in data['refer']:
                    data['refer'][user_id] = True
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, text='❌ You not Joined')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
                msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n"
                for channel in CHANNELS:
                    msg_start += f"➡️ {channel}\n"
                msg_start += f"➡️ و يجب عليك الاشتراك في قناتي على اليوتيوب:\n{YOUTUBE_CHANNEL_URL}\n"
                msg_start += "*"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, "حدث خطأ، يرجى الانتظار حتى يتم إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

@bot.message_handler(content_types=['text'])
def send_text(message):
    user_id = str(message.chat.id)
    try:
        data = json.load(open('users.json', 'r'))

        if message.text == '🆔 Account':
            accmsg = '*👮 User : {}\n\n⚙️ Wallet : *`{}`*\n\n💸 Balance : *`{}`* نقاط*'
            wallet = data.get('wallet', {}).get(user_id, "none")
            balance = data.get('balance', {}).get(user_id, 0)
            msg = accmsg.format(message.from_user.first_name, wallet, balance)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == '🙌🏻 Referrals':
            ref_msg = "*⏯️ Total Invites : {} Users\n\n👥 Refferrals System\n\n1 Level:\n🥇 Level°1 - {} نقاط\n\n🔗 Referral Link ⬇️\n{}*"
            bot_name = bot.get_me().username
            ref = data.get('referred', {}).get(user_id, 0)
            total_ref = data['total']
            link = f"https://t.me/{bot_name}?start={user_id}"
            refmsg = ref_msg.format(total_ref, ref, link)
            bot.send_message(message.chat.id, refmsg, parse_mode="Markdown")

        elif message.text == '🎁 Bonus':
            if user_id not in data['checkin']:
                data['checkin'][user_id] = 0
            if data['checkin'][user_id] < 1:
                data['balance'][user_id] += Daily_bonus
                data['checkin'][user_id] += 1
                json.dump(data, open('users.json', 'w'))
                bot.send_message(user_id, f"تم إضافة نقاطك اليومية: {Daily_bonus} نقاط")
            else:
                bot.send_message(user_id, "لقد حصلت على نقاطك اليومية بالفعل!")

        elif message.text == '💸 Withdraw':
            balance = data.get('balance', {}).get(user_id, 0)
            if balance < Mini_Withdraw:
                bot.send_message(user_id, f"الحد الأدنى للسحب هو {Mini_Withdraw} نقاط")
            else:
                # إضافة كود لإجراء عملية السحب هنا
                bot.send_message(user_id, "تم طلب السحب بنجاح!")

        elif message.text == '⚙️ Set Wallet':
            bot.send_message(message.chat.id, "يرجى إدخال عنوان محفظتك:")
            bot.register_next_step_handler(message, set_wallet)

        elif message.text == '📊 Statistics':
            if user_id == str(OWNER_ID):
                total_users = data['total']
                total_balance = sum(data['balance'].values())
                stat_msg = f"🧑‍🤝‍🧑 Total Users: {total_users}\n💰 Total Balance: {total_balance} نقاط"
                bot.send_message(user_id, stat_msg)
            else:
                bot.send_message(user_id, "ليس لديك إذن للوصول إلى الإحصائيات!")

        elif message.text == '🎮 Play Games':
            games_menu(user_id)

        menu(message.chat.id)

    except Exception as e:
        bot.send_message(message.chat.id, "هذا الأمر به خطأ، يرجى الانتظار حتى يتم إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

def games_menu(user_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🎲 Guess the Number', '🔢 Count to 10', '🔙 Back')
    bot.send_message(user_id, "*🎮 Choose a Game:*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def handle_game_selection(message):
    user_id = str(message.chat.id)

    if message.text == '🎲 Guess the Number':
        start_guessing_game(user_id)

    elif message.text == '🔢 Count to 10':
        start_counting_game(user_id)

    elif message.text == '🔙 Back':
        menu(user_id)

def start_guessing_game(user_id):
    number_to_guess = random.randint(1, 10)
    bot.send_message(user_id, "تخمين الرقم من 1 إلى 10. لديك 3 محاولات. ابدأ بالتخمين!")
    bot.register_next_step_handler_by_chat_id(user_id, lambda msg: guess_number(msg, number_to_guess, 3))

def guess_number(message, number_to_guess, attempts):
    user_id = str(message.chat.id)

    if attempts > 0:
        if message.text.isdigit() and int(message.text) == number_to_guess:
            bot.send_message(user_id, "🎉 أحسنت! لقد خمّنت الرقم الصحيح!")
            menu(user_id)
        else:
            attempts -= 1
            bot.send_message(user_id, f"😢 خاطئ! لديك {attempts} محاولة/محاولات متبقية.")
            bot.register_next_step_handler(message, lambda msg: guess_number(msg, number_to_guess, attempts))
    else:
        bot.send_message(user_id, f"💔 لقد انتهت محاولاتك! الرقم كان: {number_to_guess}.")
        menu(user_id)

def start_counting_game(user_id):
    bot.send_message(user_id, "🔢 ابدأ العد حتى 10. اكتب الرقم التالي!")
    bot.register_next_step_handler_by_chat_id(user_id, count_to_ten)

def count_to_ten(message):
    user_id = str(message.chat.id)

    if message.text.isdigit() and int(message.text) == 1:
        bot.send_message(user_id, "2")
        bot.register_next_step_handler_by_chat_id(user_id, lambda msg: count_to_ten_helper(msg, 3))
    else:
        bot.send_message(user_id, "😢 يجب أن تبدأ العد من 1.")
        menu(user_id)

def count_to_ten_helper(message, next_number):
    user_id = str(message.chat.id)

    if next_number <= 10:
        if message.text.isdigit() and int(message.text) == next_number:
            bot.send_message(user_id, str(next_number + 1))
            bot.register_next_step_handler(message, lambda msg: count_to_ten_helper(msg, next_number + 1))
        else:
            bot.send_message(user_id, f"😢 خاطئ! الرقم التالي كان: {next_number}.")
            menu(user_id)
    else:
        bot.send_message(user_id, "🎉 أحسنت! لقد أكملت العد حتى 10.")
        menu(user_id)

def set_wallet(message):
    user_id = str(message.chat.id)
    wallet_address = message.text

    data = json.load(open('users.json', 'r'))
    data['wallet'][user_id] = wallet_address
    json.dump(data, open('users.json', 'w'))

    bot.send_message(user_id, f"تم تعيين محفظتك: {wallet_address}")
    menu(user_id)

bot.polling(none_stop=True)
