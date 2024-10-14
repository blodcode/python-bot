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

            # تأكد من وجود المستخدم في القاموس
            if user_id not in data['checkin']:
                data['checkin'][user_id] = 0

            # التحقق مما إذا كان المستخدم قد استلم البونص اليومي من قبل
            if data['checkin'][user_id] < 1:  # استلام البونص مرة واحدة في اليوم
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
