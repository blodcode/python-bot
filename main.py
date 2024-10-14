import time
import json
import telebot

# توكن البوت
TOKEN = "TON"
BOT_TOKEN = "8148048276:AAG7Bw7OHeru80X_Fa_x-vHiI61WaxrX4jM"
PAYMENT_CHANNEL = "@tastttast"
OWNER_ID = 1002163515274
CHANNELS = ["@tastttast"]
Daily_bonus = 2  # تم تغيير المكافأة اليومية إلى 2 نقطة
Mini_Withdraw = 1000  # الحد الأدنى للسحب 1000 نقطة
Per_Refer = 3  # المكافأة لكل إحالة 3 نقاط

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
    keyboard.row('🆔 حسابي')
    keyboard.row('🙌🏻 إحالات', '🎁 مكافأة', '💸 سحب')
    keyboard.row('⚙️ ضبط المحفظة', '📊 إحصائيات')
    bot.send_message(id, "*🏡 الرئيسية*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        user = str(user)
        data = json.load(open('users.json', 'r'))

        # إعداد بيانات المستخدم
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
        markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ انضممت', callback_data='check'))
        msg_start = "*🍔 لاستخدام هذا البوت تحتاج إلى الانضمام إلى هذه القناة - "
        for i in CHANNELS:
            msg_start += f"\n➡️ {i}\n"
        msg_start += "*"
        bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markup)

    except:
        bot.send_message(message.chat.id, "يبدو أن هناك خطأ، يرجى الانتظار لحين إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "حدث خطأ في البوت، يرجى إصلاحه سريعًا!\n الخطأ في الأمر: " + message.text)
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
                bot.answer_callback_query(callback_query_id=call.id, text='✅ لقد انضممت الآن يمكنك كسب النقاط')
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
                        bot.send_message(ref_id, f"*🏧 إحالة جديدة في المستوى 1، لقد حصلت على: +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                    else:
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                else:
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='❌ لم تنضم بعد')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ انضممت', callback_data='check'))
                msg_start = "*🍔 لاستخدام هذا البوت تحتاج إلى الانضمام إلى هذه القناة - \n➡️ @ Fill your channels at line: 101 and 157*"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(call.message.chat.id, "يبدو أن هناك خطأ، يرجى الانتظار لحين إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "حدث خطأ في البوت، يرجى إصلاحه سريعًا!\n الخطأ في الأمر: " + call.data)
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 حسابي':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 المستخدم: {}\n\n⚙️ المحفظة: *`{}`*\n\n💸 الرصيد: *`{}`* {TOKEN}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"

            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name, wallet, balance)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        if message.text == '🙌🏻 إحالات':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ إجمالي الدعوات: {} مستخدمين\n\n👥 نظام الإحالات\n\n1 مستوى:\n🥇 مستوى°1 - {} {}*\n\n🔗 رابط الإحالة ⬇️\n{}*"

            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['referred']:
                data['referred'][user] = 0
            json.dump(data, open('users.json', 'w'))

            ref_count = data['referred'][user]
            ref_link = 'https://telegram.me/{}?start={}'.format(bot_name, message.chat.id)
            msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        if message.text == "⚙️ ضبط المحفظة":
            user_id = message.chat.id
            user = str(user_id)

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 إلغاء')
            send = bot.send_message(message.chat.id, "_⚠️ أرسل عنوان محفظتك._", parse_mode="Markdown", reply_markup=keyboard)
            bot.register_next_step_handler(message, trx_address)

        if message.text == "🎁 مكافأة":
            user_id = message.chat.id
            user = str(user_id)
            cur_time = int((time.time()))
            data = json.load(open('users.json', 'r'))

            if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 60 * 60 * 24):
                data['balance'][user] += Daily_bonus
                bot.send_message(user_id, f"مبروك! لقد حصلت على مكافأة يومية: +{Daily_bonus} {TOKEN}")
                bonus[user_id] = cur_time
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(message.chat.id, "❌ *يمكنك المطالبة بالمكافأة مرة واحدة فقط كل 24 ساعة!*", parse_mode="markdown")
            return

        if message.text == "📊 إحصائيات" and message.chat.id == OWNER_ID:  # إحصائيات للمشرفين فقط
            data = json.load(open('users.json', 'r'))
            total_users = data['total']
            total_referred = sum(data['referred'].values())
            total_balance = sum(data['balance'].values())
            
            stats_msg = f"*👥 إجمالي المستخدمين: {total_users}\n\n📈 إجمالي الإحالات: {total_referred}\n\n💰 إجمالي الرصيد: {total_balance} {TOKEN}*"
            bot.send_message(message.chat.id, stats_msg, parse_mode="Markdown")

        if message.text == "💸 سحب":
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('users.json', 'r'))

            if user not in data['balance']:
                data['balance'][user] = 0

            balance = data['balance'][user]
            if balance >= Mini_Withdraw:
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('🚫 إلغاء')
                send = bot.send_message(message.chat.id, "_⚠️ أدخل المبلغ الذي تريد سحبه._", parse_mode="Markdown", reply_markup=keyboard)
                bot.register_next_step_handler(send, withdraw_amount)
            else:
                bot.send_message(message.chat.id, f"🚫 *يجب أن يكون رصيدك أكبر من {Mini_Withdraw} {TOKEN} لتتمكن من السحب.*", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, "يبدو أن هناك خطأ، يرجى الانتظار لحين إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, f"حدث خطأ في البوت، يرجى إصلاحه سريعًا!\n الخطأ: {str(e)}")
        return

def trx_address(message):
    user_id = message.chat.id
    user = str(user_id)
    address = message.text
    data = json.load(open('users.json', 'r'))

    if message.text == '🚫 إلغاء':
        bot.send_message(message.chat.id, "✅ تم إلغاء العملية.")
        return

    data['wallet'][user] = address
    json.dump(data, open('users.json', 'w'))
    bot.send_message(message.chat.id, f"✅ تم ضبط عنوان المحفظة الخاص بك على: {address}")

def withdraw_amount(message):
    user_id = message.chat.id
    user = str(user_id)
    amount = message.text

    try:
        amount = int(amount)
        data = json.load(open('users.json', 'r'))

        if amount < Mini_Withdraw:
            bot.send_message(user_id, f"🚫 *يجب أن يكون المبلغ أكبر من {Mini_Withdraw} {TOKEN} لتتمكن من السحب.*", parse_mode="Markdown")
            return

        if amount > data['balance'][user]:
            bot.send_message(user_id, "🚫 *لا يوجد لديك رصيد كافٍ لسحب هذا المبلغ.*", parse_mode="Markdown")
            return

        data['balance'][user] -= amount
        data['withd'][user] += amount
        json.dump(data, open('users.json', 'w'))

        bot.send_message(user_id, f"✅ تم سحب {amount} {TOKEN} بنجاح.")
    except ValueError:
        bot.send_message(user_id, "🚫 *يرجى إدخال مبلغ صحيح.*")

# بدء تشغيل البوت
bot.polling(none_stop=True)
