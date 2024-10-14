import time
import json
import telebot

## TOKEN DETAILS
TOKEN = "TON"  # يجب استبدال هذا بالتوكن الصحيح
BOT_TOKEN = "8148048276:AAG7Bw7OHeru80X_Fa_x-vHiI61WaxrX4jM"
PAYMENT_CHANNEL = "@tastttast"  # إضافة القناة هنا بما في ذلك علامة '@'
OWNER_ID = 6932047318  # أدخل معرف المشرف هنا
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

    if user_id == str(OWNER_ID):  # إذا كان المستخدم مشرف
        keyboard.row('🛠️ مكافات', '📊 إحصائياتي')  # إضافة زر المكافآت
    
    keyboard.row('🆔 احصائياتي')
    keyboard.row('🙌🏻 إحالات', '🎁 مكافأة', '💸 سحب')
    
    # زر إدخال الكود للمستخدمين العاديين
    keyboard.row('🔑 إدخال الكود')

    bot.send_message(user_id, "*🏡 الرئيسية*", parse_mode="Markdown", reply_markup=keyboard)

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
        markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ انضممت', callback_data='check'))
        msg_start = "*🍔 لاستخدام هذا البوت، تحتاج إلى الانضمام إلى هذه القناة - \n"
        for channel in CHANNELS:
            msg_start += f"➡️ {channel}\n"
        msg_start += f"➡️ ويجب عليك الاشتراك في قناتي على اليوتيوب:\n{YOUTUBE_CHANNEL_URL}\n"
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
                bot.answer_callback_query(call.id, text='✅ لقد انضممت، الآن يمكنك كسب المال')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user_id not in data['refer']:
                    data['refer'][user_id] = True
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, text='❌ لم تنضم بعد')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ انضممت', callback_data='check'))
                msg_start = "*🍔 لاستخدام هذا البوت، تحتاج إلى الانضمام إلى هذه القناة - \n"
                for channel in CHANNELS:
                    msg_start += f"➡️ {channel}\n"
                msg_start += f"➡️ ويجب عليك الاشتراك في قناتي على اليوتيوب:\n{YOUTUBE_CHANNEL_URL}\n"
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

        if message.text == '🆔 احصائياتي':
            accmsg = '*👮 المستخدم : {}\n\n⚙️ المحفظة : *`{}`*\n\n💸 الرصيد : *`{}`* نقاط*'
            wallet = data.get('wallet', {}).get(user_id, "none")
            balance = data.get('balance', {}).get(user_id, 0)
            msg = accmsg.format(message.from_user.first_name, wallet, balance)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == '🙌🏻 إحالات':
            ref_msg = "*⏯️ إجمالي الدعوات : {} مستخدم\n\n👥 نظام الإحالات\n\n1 مستوى:\n🥇 المستوى°1 - {} نقاط\n\n🔗 رابط الإحالة ⬇️\n{}*"
            bot_name = bot.get_me().username
            ref = data.get('referred', {}).get(user_id, 0)
            total_ref = data['total']
            link = f"https://t.me/{bot_name}?start={user_id}"
            refmsg = ref_msg.format(total_ref, ref, link)
            bot.send_message(message.chat.id, refmsg, parse_mode="Markdown")

        elif message.text == '🎁 مكافأة':
            if user_id not in data['checkin']:
                data['checkin'][user_id] = 0
            if data['checkin'][user_id] < 1:
                data['balance'][user_id] += Daily_bonus
                data['checkin'][user_id] += 1
                json.dump(data, open('users.json', 'w'))
                bot.send_message(user_id, f"تم إضافة نقاطك اليومية: {Daily_bonus} نقاط")
            else:
                bot.send_message(user_id, "لقد حصلت على نقاطك اليومية بالفعل!")

        elif message.text == '💸 سحب':
            balance = data.get('balance', {}).get(user_id, 0)
            if balance < Mini_Withdraw:
                bot.send_message(user_id, f"الحد الأدنى للسحب هو {Mini_Withdraw} نقاط")
            else:
                # إضافة كود لإجراء عملية السحب هنا
                bot.send_message(user_id, "تم طلب السحب بنجاح!")

        elif message.text == '⚙️ إعداد المحفظة':
            bot.send_message(message.chat.id, "يرجى إدخال عنوان محفظتك:")
            bot.register_next_step_handler(message, set_wallet)

        elif message.text == '📊 إحصائياتي':
            if user_id == str(OWNER_ID):
                total_users = data['total']
                total_balance = sum(data['balance'].values())
                stat_msg = f"🧑‍🤝‍🧑 إجمالي المستخدمين: {total_users}\n💰 إجمالي الرصيد: {total_balance} نقاط"
                bot.send_message(user_id, stat_msg)
            else:
                bot.send_message(user_id, "ليس لديك إذن للوصول إلى الإحصائيات!")

        elif message.text == '🛠️ مكافات':
            if user_id == str(OWNER_ID):
                bot.send_message(user_id, "يرجى إدخال عدد النقاط والمستخدمين المسموح لهم:")
                bot.register_next_step_handler(message, create_code)
            else:
                bot.send_message(user_id, "ليس لديك إذن للوصول إلى هذه الميزة!")

        elif message.text == '🔑 إدخال الكود':
            bot.send_message(user_id, "يرجى إدخال الكود:")
            bot.register_next_step_handler(message, enter_code)

        menu(message.chat.id)

    except Exception as e:
        bot.send_message(message.chat.id, "هذا الأمر به خطأ، يرجى الانتظار حتى يتم إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

def set_wallet(message):
    user_id = str(message.chat.id)
    wallet_address = message.text.strip()
    data = json.load(open('users.json', 'r'))

    if user_id in data['wallet']:
        data['wallet'][user_id] = wallet_address
    else:
        data['wallet'] = {user_id: wallet_address}

    json.dump(data, open('users.json', 'w'))
    bot.send_message(user_id, f"تم إعداد محفظتك: {wallet_address}")

def create_code(message):
    user_id = str(message.chat.id)
    try:
        points, user_limit = map(int, message.text.split())
        code = f"CODE{int(time.time())}"  # كود فريد يعتمد على الوقت
        data = json.load(open('users.json', 'r'))

        if 'codes' not in data:
            data['codes'] = {}
        
        data['codes'][code] = {'points': points, 'user_limit': user_limit, 'used': 0}
        json.dump(data, open('users.json', 'w'))

        bot.send_message(user_id, f"تم إنشاء الكود بنجاح: {code}\nالمستخدمين المسموح لهم: {user_limit}\nالنقاط الممنوحة: {points}")
    except Exception as e:
        bot.send_message(user_id, "يرجى إدخال عدد النقاط والمستخدمين المسموح لهم بشكل صحيح (مثال: 10 5).")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

def enter_code(message):
    user_id = str(message.chat.id)
    code = message.text.strip()
    data = json.load(open('users.json', 'r'))

    if 'codes' in data and code in data['codes']:
        code_data = data['codes'][code]
        if code_data['used'] < code_data['user_limit']:
            data['balance'][user_id] += code_data['points']
            code_data['used'] += 1
            json.dump(data, open('users.json', 'w'))
            bot.send_message(user_id, f"تم استخدام الكود بنجاح! حصلت على {code_data['points']} نقاط.")
        else:
            bot.send_message(user_id, "آسف، تم استخدام هذا الكود للحد الأقصى من المستخدمين.")
    else:
        bot.send_message(user_id, "الكود غير صحيح أو غير موجود.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
