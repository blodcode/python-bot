import time
import json
import telebot

##TOKEN DETAILS
TOKEN = "TON"

BOT_TOKEN = "8148048276:AAG7Bw7OHeru80X_Fa_x-vHiI61WaxrX4jM"
PAYMENT_CHANNEL = "@tastttast"  # إضافة قناة الدفع هنا بما في ذلك علامة '@'
OWNER_ID = 1002163515274  # اكتب معرف صاحب الحساب هنا.. احصل عليه من @MissRose_Bot بواسطة /id
CHANNELS = ["@tastttast"]  # أضف القنوات التي سيتم التحقق منها هنا بتنسيق - ["القناة 1", "القناة 2"] 
                          # يمكنك إضافة العديد من القنوات هنا وأيضاً إضافة علامة '@' قبل اسم مستخدم القناة
Daily_bonus = 1  # ضع مقدار المكافأة اليومية هنا!
Mini_Withdraw = 1000  # أزل الصفر وأضف الحد الأدنى من السحب الذي تريده
Per_Refer = 4  # أضف مكافأة الإحالة هنا

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 الحساب')
    keyboard.row('🙌🏻 الإحالات', '🎁 المكافأة', '💸 سحب')
    keyboard.row('⚙️ إعداد المحفظة', '📊 الإحصائيات')
    bot.send_message(id, "*🏡 الرئيسية*", parse_mode="Markdown",
                     reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('users.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] += 1
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = "0"
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ انضممت', callback_data='check'))
            msg_start = "*🍔 لاستخدام هذا البوت، تحتاج إلى الانضمام إلى هذه القناة - "
            for i in CHANNELS:
                msg_start += f"\n➡️ {i}\n"
            msg_start += "*"
            bot.send_message(user, msg_start,
                             parse_mode="Markdown", reply_markup=markup)
        else:
            data = json.load(open('users.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] += 1
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ انضممت', callback_data='check'))
            msg_start = "*🍔 لاستخدام هذا البوت، تحتاج إلى الانضمام إلى هذه القناة - \n➡️ @ املأ قنواتك في السطر: 101 و 157*"
            bot.send_message(user, msg_start,
                             parse_mode="Markdown", reply_markup=markups)
    except:
        bot.send_message(message.chat.id, "يوجد خطأ في هذه الرسالة، يرجى الانتظار حتى يتم إصلاح العطل من قبل الإدارة.")
        bot.send_message(OWNER_ID, "لقد حدث خطأ في البوت الخاص بك، يرجى إصلاحه بسرعة!\n الخطأ في الأمر: " + message.text)
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(
                    callback_query_id=call.id, text='✅ لقد انضممت الآن، يمكنك كسب المال')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user not in data['refer']:
                    data['refer'][user] = True
                    if user not in data['referby']:
                        data['referby'][user] = user
                        json.dump(data, open('users.json', 'w'))
                    if int(data['referby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)
                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0
                        json.dump(data, open('users.json', 'w'))
                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1
                        bot.send_message(
                            ref_id, f"*🏧 إحالة جديدة في المستوى 1، لقد حصلت على : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                    else:
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                else:
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(
                    callback_query_id=call.id, text='❌ لم تنضم')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(
                    text='🤼‍♂️ انضممت', callback_data='check'))
                msg_start = "*🍔 لاستخدام هذا البوت، تحتاج إلى الانضمام إلى هذه القناة - \n➡️ @ املأ قنواتك في السطر: 101 و 157*"
                bot.send_message(call.message.chat.id, msg_start,
                                 parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(call.message.chat.id, "يوجد خطأ في هذه الرسالة، يرجى الانتظار حتى يتم إصلاح العطل من قبل الإدارة.")
        bot.send_message(OWNER_ID, "لقد حدث خطأ في البوت الخاص بك، يرجى إصلاحه بسرعة!\n الخطأ في الأمر: " + call.data)
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 الحساب':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 المستخدم : {}\n\n⚙️ المحفظة : *`{}`*\n\n💸 الرصيد : *`{}`* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"

            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name,
                                wallet, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        if message.text == '🙌🏻 الإحالات':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ الإحالات*\n\n"
            user_id = message.chat.id
            user = str(user_id)
            if user not in data['referby']:
                data['referby'][user] = user
            total_ref = data['referred'][user]

            ref_msg += f"عدد الإحالات: *{total_ref}*"

            bot.send_message(message.chat.id, ref_msg, parse_mode="Markdown")
        if message.text == '🎁 المكافأة':
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            user = str(user_id)
            if user not in bonus:
                bonus[user] = 0
            if bonus[user] == 0:
                bonus[user] += 1
                data['balance'][user] += Daily_bonus
                bot.send_message(message.chat.id,
                                 f"*🎁 تم إضافة مكافأتك اليومية! رصيدك الآن هو: `{data['balance'][user]}` {TOKEN}*", parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "*❌ لديك بالفعل مكافأة يومية*",
                                 parse_mode="Markdown")
            json.dump(data, open('users.json', 'w'))

        if message.text == '💸 سحب':
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0

            balance = data['balance'][user]

            if balance >= Mini_Withdraw:
                if user not in data['wallet']:
                    data['wallet'][user] = "none"
                bot.send_message(message.chat.id,
                                 f"*💸 أدخل عنوان محفظتك لإرسال {Mini_Withdraw} {TOKEN}*\n\n📝 *للمساعدة، يمكنك كتابة `/help`*",
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, process_withdraw)
            else:
                bot.send_message(message.chat.id,
                                 f"*❌ رصيدك ليس كافي لسحب {Mini_Withdraw} {TOKEN}*\n\n*رصيدك الحالي هو: `{balance}` {TOKEN}*",
                                 parse_mode="Markdown")

        if message.text == '⚙️ إعداد المحفظة':
            bot.send_message(message.chat.id, "*📝 أدخل عنوان محفظتك ليتم تخزينه*",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, process_wallet)

        if message.text == '📊 الإحصائيات':
            data = json.load(open('users.json', 'r'))
            total_users = data['total']
            total_referrals = sum(data['referred'].values())
            bot.send_message(message.chat.id,
                             f"*📈 الإحصائيات*\n\n*إجمالي المستخدمين: {total_users}*\n*إجمالي الإحالات: {total_referrals}*",
                             parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "يوجد خطأ في هذه الرسالة، يرجى الانتظار حتى يتم إصلاح العطل من قبل الإدارة.")
        bot.send_message(OWNER_ID, "لقد حدث خطأ في البوت الخاص بك، يرجى إصلاحه بسرعة!\n الخطأ في الأمر: " + message.text)
        return

def process_wallet(message):
    user_id = message.chat.id
    user = str(user_id)
    data = json.load(open('users.json', 'r'))

    data['wallet'][user] = message.text
    json.dump(data, open('users.json', 'w'))
    bot.send_message(message.chat.id, f"*✅ تم تخزين محفظتك: {message.text}*",
                     parse_mode="Markdown")
    menu(message.chat.id)

def process_withdraw(message):
    user_id = message.chat.id
    user = str(user_id)
    data = json.load(open('users.json', 'r'))
    balance = data['balance'][user]

    if message.text not in data['wallet'].values():
        bot.send_message(user_id, "*❌ عنوان المحفظة غير صحيح، يرجى المحاولة مرة أخرى*",
                         parse_mode="Markdown")
        bot.send_message(user_id, "*📝 أدخل عنوان محفظتك ليتم تخزينه*",
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, process_wallet)
    else:
        wallet_address = message.text
        if balance >= Mini_Withdraw:
            data['balance'][user] -= Mini_Withdraw
            data['withd'][user] += Mini_Withdraw
            bot.send_message(user_id,
                             f"*💸 تم إرسال {Mini_Withdraw} {TOKEN} إلى {wallet_address}*\n\n*رصيدك المتبقي: `{data['balance'][user]}` {TOKEN}*",
                             parse_mode="Markdown")
            json.dump(data, open('users.json', 'w'))
            # هنا يمكنك إضافة عملية إرسال النقود إلى المحفظة
        else:
            bot.send_message(user_id,
                             f"*❌ رصيدك ليس كافٍ لسحب {Mini_Withdraw} {TOKEN}*\n\n*رصيدك الحالي هو: `{balance}` {TOKEN}*",
                             parse_mode="Markdown")
            return

if __name__ == "__main__":
    bot.polling(none_stop=True)
