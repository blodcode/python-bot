import time
import json
import telebot

##TOKEN DETAILS
TOKEN = "TON"

BOT_TOKEN = "8148048276:AAG7Bw7OHeru80X_Fa_x-vHiI61WaxrX4jM"
PAYMENT_CHANNEL = "@tastttast"  # add payment channel here including the '@' sign
OWNER_ID = 6932047318  # write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@tastttast"]  # add channels to be checked here in the format - ["Channel 1", "Channel 2"]
# you can add as many channels here and also add the '@' sign before channel username
Daily_bonus = 2  # Put daily bonus amount here!
Mini_Withdraw = 1000  # remove 0 and add the minimum withdraw you want to set
Per_Refer = 3  # add per refer bonus here

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
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '🎁 Bonus', '💸 Withdraw')
    keyboard.row('⚙️ Set Wallet', '📊 Statistics')  # الإحصائيات للمشرف فقط
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

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
                data['total'] = data['total'] + 1
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
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - "
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
                data['total'] = data['total'] + 1
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
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
            bot.send_message(user, msg_start,
                             parse_mode="Markdown", reply_markup=markups)
    except Exception as e:
        bot.send_message(message.chat.id, "This command having error pls wait for fixing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: " + message.text + "\n" + str(e))
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch == True:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(
                    callback_query_id=call.id, text='✅ You joined Now you can earn money')
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
                            ref_id, f"*🏧 New Referral on Level 1, You Got : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
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
                    callback_query_id=call.id, text='❌ You not Joined')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(
                    text='🤼‍♂️ Joined', callback_data='check'))
                msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
                bot.send_message(call.message.chat.id, msg_start,
                                 parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, "This command having error pls wait for fixing the glitch by admin")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: " + call.data + "\n" + str(e))
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 Account':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 User : {}\n\n⚙️ Wallet : *`{}`*\n\n💸 Balance : *`{}`* نقاط*'
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
                                wallet, balance)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        
        if message.text == '🙌🏻 Referrals':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ Total Invites : {} Users\n\n👥 Refferrals System\n\n1 Level:\n🥇 Level°1 - {} نقاط\n\n🔗 Referral Link ⬇️\n{}*"

            bot_name = bot.get_me().username
            user_id = message.chat.id
            if user_id not in data['referred']:
                data['referred'][user_id] = 0

            ref = data['referred'][user_id]
            total_ref = data['total']
            link = f"https://t.me/{bot_name}?start={user_id}"
            json.dump(data, open('users.json', 'w'))

            refmsg = ref_msg.format(total_ref, ref, link)
            bot.send_message(message.chat.id, refmsg, parse_mode="Markdown")

        if message.text == '🎁 Bonus':
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            if user_id not in data['checkin']:
                data['checkin'][user_id] = 0
            if data['checkin'][user_id] < 1:
                data['balance'][user_id] += Daily_bonus
                data['checkin'][user_id] += 1
                json.dump(data, open('users.json', 'w'))
                bot.send_message(user_id, f"تم اضافة نقاطك اليومية: {Daily_bonus} نقاط")
            else:
                bot.send_message(user_id, "لقد حصلت على نقاطك اليومية بالفعل!")

        if message.text == '💸 Withdraw':
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            if user_id not in data['balance']:
                data['balance'][user_id] = 0
            if user_id not in data['withd']:
                data['withd'][user_id] = 0

            balance = data['balance'][user_id]
            if balance < Mini_Withdraw:
                bot.send_message(user_id, f"الحد الأدنى للسحب هو {Mini_Withdraw} نقاط")
            else:
                # هنا يمكنك إضافة كود لإجراء عملية السحب
                bot.send_message(user_id, "تم طلب السحب بنجاح!")

        if message.text == '📊 Statistics':
            user_id = message.chat.id
            if user_id == OWNER_ID:
                data = json.load(open('users.json', 'r'))
                total_users = data['total']
                total_balance = sum(data['balance'].values())
                stat_msg = f"🧑‍🤝‍🧑 Total Users: {total_users}\n💰 Total Balance: {total_balance} نقاط"
                bot.send_message(user_id, stat_msg)
            else:
                bot.send_message(user_id, "ليس لديك إذن للوصول إلى الإحصائيات!")

        menu(message.chat.id)

    except Exception as e:
        bot.send_message(message.chat.id, "هذا الأمر به خطأ، يرجى الانتظار حتى يتم إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "لقد واجه البوت خطأ، يرجى إصلاحه بسرعة!\nخطأ في الأمر: " + message.text + "\n" + str(e))
        return

bot.polling(none_stop=True)
