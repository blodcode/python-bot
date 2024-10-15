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
    keyboard.row('احصائياتي')  # Changed to Egyptian Arabic
    keyboard.row('🙌🏻 الإحالات', '🎁 مكافآت', '💸 السحب', '📝 المهام')  # Added tasks button
    keyboard.row('⚙️ إعداد المحفظة')  # Removed Statistics button for regular users
    if user_id == OWNER_ID:  # Show statistics only for the admin
        keyboard.row('📊 إحصائيات', '🛠️ وضع المهام')  # Added set tasks button for admin
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
        if user_id not in data['tasks_completed']:  # Initialize tasks_completed
            data['tasks_completed'][user_id] = 0  # Initialize tasks_completed for new user
        json.dump(data, open('users.json', 'w'))

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ انضممت', callback_data='check'))
        msg_start = "*🍔 لاستخدام هذا البوت، يجب عليك الانضمام إلى هذه القناة - \n"
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
                bot.answer_callback_query(call.id, text='✅ لقد انضممت، الآن يمكنك كسب النقاط')
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
                msg_start = "*🍔 لاستخدام هذا البوت، يجب عليك الانضمام إلى هذه القناة - \n"
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

        if message.text == 'احصائياتي':
            accmsg = '*👮 المستخدم : {}\n\n⚙️ المحفظة : *`{}`*\n\n💸 الرصيد : *`{}`* نقاط*'
            wallet = data.get('wallet', {}).get(user_id, "none")
            balance = data.get('balance', {}).get(user_id, 0)
            msg = accmsg.format(message.from_user.first_name, wallet, balance)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == '🙌🏻 الإحالات':
            ref_msg = "*⏯️ إجمالي الدعوات : {} مستخدمين\n\n👥 نظام الإحالات\n\n1 مستوى:\n🥇 المستوى °1 - {} نقاط\n\n🔗 رابط الإحالة ⬇️\n{}*"
            bot_name = bot.get_me().username
            ref = data.get('referred', {}).get(user_id, 0)
            total_ref = data['total']
            link = f"https://t.me/{bot_name}?start={user_id}"
            refmsg = ref_msg.format(total_ref, ref, link)
            bot.send_message(message.chat.id, refmsg, parse_mode="Markdown")

        elif message.text == '🎁 مكافآت':
            if user_id not in data['checkin']:
                data['checkin'][user_id] = 0
            if data['checkin'][user_id] < 1:
                data['balance'][user_id] += Daily_bonus
                data['checkin'][user_id] += 1
                json.dump(data, open('users.json', 'w'))
                bot.send_message(user_id, f"تم إضافة نقاطك اليومية: {Daily_bonus} نقاط")
            else:
                bot.send_message(user_id, "لقد حصلت على نقاطك اليومية بالفعل!")

        elif message.text == '💸 السحب':
            balance = data.get('balance', {}).get(user_id, 0)
            if balance < Mini_Withdraw:
                bot.send_message(user_id, f"الحد الأدنى للسحب هو {Mini_Withdraw} نقاط")
            else:
                # إضافة كود لإجراء عملية السحب هنا
                bot.send_message(user_id, "تم طلب السحب بنجاح!")

        elif message.text == '⚙️ إعداد المحفظة':
            bot.send_message(message.chat.id, "يرجى إدخال عنوان محفظتك:")
            bot.register_next_step_handler(message, set_wallet)

        elif message.text == '📊 إحصائيات':
            if user_id == str(OWNER_ID):
                total_users = data['total']
                total_balance = sum(data['balance'].values())
                stat_msg = f"🧑‍🤝‍🧑 إجمالي المستخدمين: {total_users}\n💰 إجمالي الرصيد: {total_balance} نقاط"
                bot.send_message(user_id, stat_msg)
            else:
                bot.send_message(user_id, "ليس لديك إذن للوصول إلى الإحصائيات!")

        elif message.text == '📝 المهام':
            tasks_msg = "*📋 المهام المتاحة:\n\n"
            tasks = data.get('tasks', {})
            if tasks:
                for task, points in tasks.items():
                    tasks_msg += f"- {task}: {points} نقاط\n"
            else:
                tasks_msg += "لا توجد مهام متاحة في الوقت الحالي."
            bot.send_message(user_id, tasks_msg, parse_mode="Markdown")

        elif message.text.startswith('إكمال المهمة:'):
            task_name = message.text.replace('إكمال المهمة:', '').strip()
            if task_name in data.get('tasks', {}):
                if user_id not in data['tasks_completed']:
                    data['tasks_completed'][user_id] = []
                if task_name not in data['tasks_completed'][user_id]:
                    data['balance'][user_id] += data['tasks'][task_name]
                    data['tasks_completed'][user_id].append(task_name)
                    json.dump(data, open('users.json', 'w'))
                    bot.send_message(user_id, f"تم إكمال المهمة: {task_name} +{data['tasks'][task_name]} نقاط")
                else:
                    bot.send_message(user_id, "لقد أكملت هذه المهمة بالفعل!")
            else:
                bot.send_message(user_id, "هذه المهمة غير موجودة.")

        elif message.text == '🛠️ وضع المهام':
            if user_id == str(OWNER_ID):
                bot.send_message(message.chat.id, "يرجى إدخال اسم المهمة و عدد النقاط (مثال: مهمة1: 5):")
                bot.register_next_step_handler(message, set_task)
            else:
                bot.send_message(user_id, "ليس لديك إذن لوضع المهام!")

        else:
            bot.send_message(user_id, "غير مفهوم، يرجى اختيار خيار صحيح.")
    except Exception as e:
        bot.send_message(message.chat.id, "حدث خطأ، يرجى الانتظار حتى يتم إصلاحه من قبل المسؤول.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

def set_wallet(message):
    user_id = str(message.chat.id)
    try:
        data = json.load(open('users.json', 'r'))
        data['wallet'][user_id] = message.text
        json.dump(data, open('users.json', 'w'))
        bot.send_message(user_id, "تم تحديث عنوان المحفظة بنجاح.")
    except Exception as e:
        bot.send_message(user_id, "حدث خطأ أثناء تحديث المحفظة.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

def set_task(message):
    user_id = str(message.chat.id)
    try:
        data = json.load(open('users.json', 'r'))
        task_info = message.text.split(":")
        if len(task_info) == 2:
            task_name = task_info[0].strip()
            task_points = int(task_info[1].strip())
            if 'tasks' not in data:
                data['tasks'] = {}
            data['tasks'][task_name] = task_points
            json.dump(data, open('users.json', 'w'))
            bot.send_message(user_id, f"تم إضافة المهمة: {task_name} بمقدار {task_points} نقاط.")
        else:
            bot.send_message(user_id, "يرجى إدخال صيغة صحيحة (مثال: مهمة1: 5).")
    except Exception as e:
        bot.send_message(user_id, "حدث خطأ أثناء إضافة المهمة.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

# Start the bot
bot.polling(none_stop=True)
