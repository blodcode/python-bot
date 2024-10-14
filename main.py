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
    keyboard.row('احصائياتي')
    keyboard.row('احالات', 'هدية يومية', 'سحب')
    keyboard.row('ضبط المحفظة', '📊 احصائيات' if str(user_id) == str(OWNER_ID) else '')
    keyboard.row('مكافات' if str(user_id) == str(OWNER_ID) else '')  # زر المكافآت للمشرف فقط
    bot.send_message(user_id, "*🏡 القائمة الرئيسية*", parse_mode="Markdown", reply_markup=keyboard)

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
        markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ اشتركت', callback_data='check'))
        msg_start = "*🍔 علشان تستخدم البوت، لازم تشترك في القنوات دي - \n"
        for channel in CHANNELS:
            msg_start += f"➡️ {channel}\n"
        msg_start += f"➡️ و لازم تشترك في قناتي على اليوتيوب:\n{YOUTUBE_CHANNEL_URL}\n"
        msg_start += "*"
        bot.send_message(user_id, msg_start, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, "فيه مشكلة، كلم الأدمن وهيساعدك.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                bot.answer_callback_query(call.id, text='✅ اشتركت، دلوقتي ممكن تكسب نقاط.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user_id not in data['refer']:
                    data['refer'][user_id] = True
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(call.id, text='❌ مش مشترك في القنوات.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ اشتركت', callback_data='check'))
                msg_start = "*🍔 علشان تستخدم البوت، لازم تشترك في القنوات دي - \n"
                for channel in CHANNELS:
                    msg_start += f"➡️ {channel}\n"
                msg_start += f"➡️ و لازم تشترك في قناتي على اليوتيوب:\n{YOUTUBE_CHANNEL_URL}\n"
                msg_start += "*"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, "فيه مشكلة، كلم الأدمن وهيساعدك.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

@bot.message_handler(content_types=['text'])
def send_text(message):
    user_id = str(message.chat.id)
    try:
        data = json.load(open('users.json', 'r'))

        if message.text == 'احصائياتي':
            accmsg = '*👮 الاسم : {}\n\n⚙️ المحفظة : *`{}`*\n\n💸 الرصيد : *`{}`* نقاط*'
            wallet = data.get('wallet', {}).get(user_id, "none")
            balance = data.get('balance', {}).get(user_id, 0)
            msg = accmsg.format(message.from_user.first_name, wallet, balance)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == 'احالات':
            ref_msg = "*⏯️ إجمالي الدعوات : {} مستخدمين\n\n👥 نظام الإحالات\n\n1 مستوى:\n🥇 المستوى°1 - {} نقاط\n\n🔗 رابط الإحالة ⬇️\n{}*"
            bot_name = bot.get_me().username
            ref = data.get('referred', {}).get(user_id, 0)
            total_ref = data['total']
            link = f"https://t.me/{bot_name}?start={user_id}"
            refmsg = ref_msg.format(total_ref, ref, link)
            bot.send_message(message.chat.id, refmsg, parse_mode="Markdown")

        elif message.text == 'هدية يومية':
            if user_id not in data['checkin']:
                data['checkin'][user_id] = 0
            if data['checkin'][user_id] < 1:
                data['balance'][user_id] += Daily_bonus
                data['checkin'][user_id] += 1
                json.dump(data, open('users.json', 'w'))
                bot.send_message(user_id, f"تم إضافة {Daily_bonus} نقاط لهديتك اليومية.")
            else:
                bot.send_message(user_id, "أنت بالفعل أخذت نقاط الهديتك اليومية!")

        elif message.text == 'سحب':
            balance = data.get('balance', {}).get(user_id, 0)
            if balance < Mini_Withdraw:
                bot.send_message(user_id, f"الحد الأدنى للسحب هو {Mini_Withdraw} نقاط.")
            else:
                # إضافة كود السحب هنا
                bot.send_message(user_id, "تم طلب السحب بنجاح!")

        elif message.text == 'ضبط المحفظة':
            bot.send_message(message.chat.id, "اكتب عنوان محفظتك:")
            bot.register_next_step_handler(message, set_wallet)

        elif message.text == '📊 احصائيات':
            if user_id == str(OWNER_ID):
                total_users = data['total']
                total_balance = sum(data['balance'].values())
                stat_msg = f"🧑‍🤝‍🧑 إجمالي المستخدمين: {total_users}\n💰 إجمالي الرصيد: {total_balance} نقاط"
                bot.send_message(user_id, stat_msg)
            else:
                bot.send_message(user_id, "أنت مش مشرف، مش مسموحلك تشوف الإحصائيات!")

        elif message.text == 'مكافات':
            if user_id == str(OWNER_ID):
                bot.send_message(user_id, "اكتب عدد النقاط لكل رابط:")
                bot.register_next_step_handler(message, set_rewards_points)

        menu(message.chat.id)

    except Exception as e:
        bot.send_message(message.chat.id, "فيه مشكلة في الأمر ده، كلم الأدمن وهيساعدك.")
        bot.send_message(OWNER_ID, "خطأ في البوت: " + str(e))

def set_wallet(message):
    user_id = str(message.chat.id)
    wallet_address = message.text.strip()

    # تحديث عنوان المحفظة في البيانات
    data = json.load(open('users.json', 'r'))
    if user_id in data['wallet']:
        data['wallet'][user_id] = wallet_address
    else:
        data['wallet'][user_id] = wallet_address

    json.dump(data, open('users.json', 'w'))
    bot.send_message(user_id, f"تم تعيين عنوان المحفظة إلى: {wallet_address}")

def set_rewards_points(message):
    user_id = str(message.chat.id)
    try:
        points = int(message.text.strip())
        bot.send_message(user_id, f"حدد عدد مرات استخدام الرابط:")
        bot.register_next_step_handler(message, set_rewards_limit, points)
    except ValueError:
        bot.send_message(user_id, "يرجى إدخال عدد صحيح للنقاط.")
        bot.register_next_step_handler(message, set_rewards_points)

def set_rewards_limit(message, points):
    user_id = str(message.chat.id)
    try:
        limit = int(message.text.strip())
        # توليد رابط المكافأة وإرساله
        reward_link = f"https://t.me/{bot.get_me().username}?start=reward_{points}_{limit}"
        bot.send_message(user_id, f"تم إنشاء رابط المكافأة: {reward_link}\nالنقاط: {points}\nعدد الاستخدامات: {limit}")
    except ValueError:
        bot.send_message(user_id, "يرجى إدخال عدد صحيح للاستخدامات.")
        bot.register_next_step_handler(message, set_rewards_limit, points)

bot.polling(none_stop=True)
