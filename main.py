import time
import json
import telebot

##TOKEN DETAILS
TOKEN = "TON"  # Updated from "TRON" to "TON"
BOT_TOKEN = "8148048276:AAG7Bw7OHeru80X_Fa_x-vHiI61WaxrX4jM"
PAYMENT_CHANNEL = "@tastttast"  # Add payment channel here including the '@' sign
OWNER_ID = 1002163515274  # Write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@tastttast"]  # Add channels to be checked here in the format - ["Channel 1", "Channel 2"] 
# You can add as many channels here and also add the '@' sign before channel username
Daily_bonus = 2  # Set daily bonus amount to 2 points
Mini_Withdraw = 1000  # Set minimum withdraw to 1000 points
Per_Refer = 3  # Set referral bonus to 3 points

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
    keyboard.row('🙌🏻 Referrals', '🎁 Points', '💸 Withdraw')
    keyboard.row('⚙️ Set Wallet')
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
            markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - "
            for i in CHANNELS:
                msg_start += f"\n➡️ {i}\n"
            msg_start += "*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markup)
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
            markups.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markups)
    except:
        bot.send_message(message.chat.id, "This command has an error. Please wait for fixing the glitch by admin.")
        bot.send_message(OWNER_ID, "Your bot encountered an error! Fix it fast!\n Error on command: " + message.text)
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
                bot.answer_callback_query(callback_query_id=call.id, text='✅ You joined, now you can earn money')
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
                        bot.send_message(ref_id, f"*🏧 New Referral on Level 1, You Got: +{Per_Refer} Points*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                    else:
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                else:
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='❌ You are not joined')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
                msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(call.message.chat.id, "This command has an error. Please wait for fixing the glitch by admin.")
        bot.send_message(OWNER_ID, "Your bot encountered an error! Fix it fast!\n Error on command: " + call.data)
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 Account':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 User: {}\n\n⚙️ Wallet: *`{}`*\n\n💸 Balance: *`{}`* Points*'
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
        
        if message.text == '🙌🏻 Referrals':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ Total Invites: {} Users\n\n👥 Referrals System\n\n1 Level:\n🥇 Level°1 - {} Points\n\n🔗 Referral Link ⬇️\n{}*"

            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['referred']:
                data['referred'][user] = 0

            ref_count = data['referred'][user]
            ref_link = f"https://t.me/{bot_name}?start={user_id}"

            msg = ref_msg.format(ref_count, Per_Refer, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        if message.text == '🎁 Points':
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            user = str(user_id)
            if user not in data['checkin']:
                data['checkin'][user] = 0
            
            if int(data['checkin'][user]) < 1:
                data['checkin'][user] = data['checkin'][user] + 1
                data['balance'][user] += Daily_bonus
                bot.send_message(user_id, f"✨ You claimed your daily bonus of: *{Daily_bonus} Points*", parse_mode="Markdown")
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(user_id, "❌ You have already claimed your daily bonus.")
        
        if message.text == '💸 Withdraw':
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            user = str(user_id)
            withdraw_msg = "*💵 Enter amount to withdraw*\n*Minimum: {} Points*".format(Mini_Withdraw)
            bot.send_message(user_id, withdraw_msg, parse_mode="Markdown")
            bot.register_next_step_handler(message, withdraw)
        
        if message.text == '⚙️ Set Wallet':
            data = json.load(open('users.json', 'r'))
            user_id = message.chat.id
            user = str(user_id)
            bot.send_message(user_id, "💰 Enter your wallet address.")
            bot.register_next_step_handler(message, set_wallet)
    except:
        bot.send_message(message.chat.id, "This command has an error. Please wait for fixing the glitch by admin.")
        bot.send_message(OWNER_ID, "Your bot encountered an error! Fix it fast!\n Error on command: " + message.text)

def withdraw(message):
    try:
        data = json.load(open('users.json', 'r'))
        user_id = message.chat.id
        user = str(user_id)

        if message.text.isdigit():
            amount = int(message.text)

            if amount >= Mini_Withdraw:
                if amount <= data['balance'][user]:
                    data['balance'][user] -= amount
                    data['withd'][user] += amount
                    bot.send_message(user_id, f"✅ Successfully withdrew: *{amount} Points* to your wallet.", parse_mode="Markdown")
                    json.dump(data, open('users.json', 'w'))
                else:
                    bot.send_message(user_id, "❌ You don't have enough balance.")
            else:
                bot.send_message(user_id, f"❌ Minimum withdraw amount is: {Mini_Withdraw} Points")
        else:
            bot.send_message(user_id, "❌ Please enter a valid amount.")
    except:
        bot.send_message(message.chat.id, "This command has an error. Please wait for fixing the glitch by admin.")
        bot.send_message(OWNER_ID, "Your bot encountered an error! Fix it fast!\n Error on command: " + message.text)

def set_wallet(message):
    try:
        data = json.load(open('users.json', 'r'))
        user_id = message.chat.id
        user = str(user_id)

        if message.text:
            data['wallet'][user] = message.text
            json.dump(data, open('users.json', 'w'))
            bot.send_message(user_id, f"✅ Wallet address set to: *{message.text}*", parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "This command has an error. Please wait for fixing the glitch by admin.")
        bot.send_message(OWNER_ID, "Your bot encountered an error! Fix it fast!\n Error on command: " + message.text)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == OWNER_ID:
        bot.send_message(message.chat.id, "Welcome to Admin Panel. Choose an option:")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('📊 User Statistics')
        bot.send_message(message.chat.id, "Select option:", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def admin_commands(message):
    if message.chat.id == OWNER_ID:
        if message.text == '📊 User Statistics':
            data = json.load(open('users.json', 'r'))
            stats_msg = "*📈 User Statistics:*\nTotal Users: {}\nTotal Balance: {}\nTotal Withdrawn: {}*".format(data['total'], sum(data['balance'].values()), sum(data['withd'].values()))
            bot.send_message(message.chat.id, stats_msg, parse_mode="Markdown")

bot.polling(none_stop=True)
