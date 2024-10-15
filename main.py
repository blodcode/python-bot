import time
import json
import telebot

## TOKEN DETAILS
TOKEN = "TON"
BOT_TOKEN = "8148048276:AAG7Bw7OHeru80X_Fa_x-vHiI61WaxrX4jM"
PAYMENT_CHANNEL = "@tastttast"
OWNER_ID = 6932047318
CHANNELS = ["@tastttast"]
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/c/YourChannelName"
Daily_bonus = 2
Mini_Withdraw = 1000
Per_Refer = 3

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for channel in CHANNELS:
        check = bot.get_chat_member(channel, id)
        if check.status == 'left':
            return False
    return True

def menu(user_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('📊 احصائياتي')
    keyboard.row('💼 المهام', '🎁 المكافآت')
    keyboard.row('🙌🏻 الإحالات', '💸 السحب')
    keyboard.row('⚙️ إعداد المحفظة')
    if user_id == OWNER_ID:
        keyboard.row('🔧 إضافة مهمة', '📊 إحصائيات المشرفين')
    bot.send_message(user_id, "*🏠 القائمة الرئيسية*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    try:
        data = json.load(open('users.json', 'r'))

        # Ensure that all necessary fields are initialized for new users
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
        if user_id not in data['tasks_completed']:
            data['tasks_completed'][user_id] = 0

        json.dump(data, open('users.json', 'w'))

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='📺 انضممت', callback_data='check'))
        msg_start = "*مرحبًا بك في البوت! \n📢 للاستخدام، يجب عليك الانضمام إلى القنوات التالية:* \n"
        for channel in CHANNELS:
            msg_start += f"➡️ {channel}\n"
        msg_start += f"➡️ *اشترك في قناتنا على اليوتيوب:*\n{YOUTUBE_CHANNEL_URL}\n"
        bot.send_message(user_id, msg_start, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, "حدث خطأ، يرجى الانتظار حتى يتم إصلاحه.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                bot.answer_callback_query(call.id, text='✅ انضممت بنجاح!')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user_id not in data['refer']:
                    data['refer'][user_id] = True
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, text='❌ لم تنضم بعد!')
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='📺 انضممت', callback_data='check'))
                msg_start = "*للشروع في الاستخدام، يرجى الانضمام إلى القنوات التالية:* \n"
                for channel in CHANNELS:
                    msg_start += f"➡️ {channel}\n"
                msg_start += f"➡️ اشترك في قناتنا على اليوتيوب:\n{YOUTUBE_CHANNEL_URL}\n"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, "حدث خطأ، يرجى الانتظار حتى يتم إصلاحه.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

@bot.message_handler(content_types=['text'])
def send_text(message):
    user_id = str(message.chat.id)
    try:
        data = json.load(open('users.json', 'r'))

        if message.text == '📊 احصائياتي':
            accmsg = '*👤 المستخدم : {}\n\n💼 المحفظة : *`{}`*\n\n💸 الرصيد : *`{}`* نقاط*'
            wallet = data.get('wallet', {}).get(user_id, "none")
            balance = data.get('balance', {}).get(user_id, 0)
            msg = accmsg.format(message.from_user.first_name, wallet, balance)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == '💼 المهام':
            bot.send_message(user_id, "هذه هي المهام المتاحة!")

        elif message.text == '🎁 المكافآت':
            # Ensure user exists in 'checkin'
            if user_id not in data['checkin']:
                data['checkin'][user_id] = 0
                json.dump(data, open('users.json', 'w'))  # Save changes if any
            
            if data['checkin'][user_id] < 1:
                data['balance'][user_id] += Daily_bonus
                data['checkin'][user_id] += 1
                json.dump(data, open('users.json', 'w'))  # Save changes
                bot.send_message(user_id, f"تم إضافة نقاطك اليومية: {Daily_bonus} نقاط")
            else:
                bot.send_message(user_id, "لقد حصلت على نقاطك اليومية بالفعل!")

        elif message.text == '💸 السحب':
            balance = data.get('balance', {}).get(user_id, 0)
            if balance < Mini_Withdraw:
                bot.send_message(user_id, f"الحد الأدنى للسحب هو {Mini_Withdraw} نقاط")
            else:
                bot.send_message(user_id, "تم طلب السحب بنجاح!")

        elif message.text == '⚙️ إعداد المحفظة':
            bot.send_message(message.chat.id, "يرجى إدخال عنوان محفظتك:")
            bot.register_next_step_handler(message, set_wallet)

        elif message.text == '📊 إحصائيات المشرفين':
            if user_id == str(OWNER_ID):
                total_users = data['total']
                total_balance = sum(data['balance'].values())
                stat_msg = f"👥 إجمالي المستخدمين: {total_users}\n💰 إجمالي الرصيد: {total_balance} نقاط"
                bot.send_message(user_id, stat_msg)
            else:
                bot.send_message(user_id, "ليس لديك إذن للوصول إلى هذه الإحصائيات!")

        elif message.text == '🔧 إضافة مهمة':
            bot.send_message(user_id, "يرجى إدخال اسم المهمة:")
            bot.register_next_step_handler(message, add_task)

        menu(message.chat.id)

    except Exception as e:
        bot.send_message(message.chat.id, "حدث خطأ، يرجى الانتظار حتى يتم إصلاحه.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

def set_wallet(message):
    user_id = str(message.chat.id)
    data = json.load(open('users.json', 'r'))
    data['wallet'][user_id] = message.text
    json.dump(data, open('users.json', 'w'))
    bot.send_message(user_id, "تم تعيين المحفظة بنجاح!")

def add_task(message):
    # Task-adding logic goes here
    bot.send_message(message.chat.id, "تم إضافة المهمة بنجاح!")

bot.polling(none_stop=True)
