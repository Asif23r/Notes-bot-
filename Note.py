import telebot
from telebot.types import Message

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

users = {}  # {user_id: {"points": 5, "ref_by": None, "ref_count": 0}}

# Command: /start or /start ref12345
@bot.message_handler(commands=['start'])
def start_handler(msg: Message):
    user_id = msg.from_user.id
    args = msg.text.split()

    if user_id not in users:
        users[user_id] = {"points": 5, "ref_by": None, "ref_count": 0}
        if len(args) == 2:
            ref_code = args[1]
            try:
                ref_id = int(ref_code.replace("ref", ""))
                if ref_id != user_id and ref_id in users:
                    users[user_id]["ref_by"] = ref_id
                    users[ref_id]["points"] += 5
                    users[ref_id]["ref_count"] += 1
                    bot.send_message(ref_id, f"🎉 Someone used your referral! +5 points")
            except:
                pass
        bot.reply_to(msg, "Welcome! You got 5 free points to access notes.")
    else:
        bot.reply_to(msg, "You already started the bot.")

# Command: /mystatus
@bot.message_handler(commands=['mystatus'])
def mystatus(msg: Message):
    user_id = msg.from_user.id
    data = users.get(user_id, {"points": 0, "ref_count": 0})
    bot.reply_to(msg, f"Points: {data['points']}\nReferrals: {data['ref_count']}")

# Command: /refer
@bot.message_handler(commands=['refer'])
def refer(msg: Message):
    user_id = msg.from_user.id
    bot.reply_to(msg, f"Your referral link:\n/start ref{user_id}")

# Command: /buypoints
@bot.message_handler(commands=['buypoints'])
def buypoints(msg: Message):
    bot.reply_to(msg, "Send ₹10 to UPI: `yourupi@upi`\nThen send /paid to confirm.")

# Command: /notes
@bot.message_handler(commands=['notes'])
def notes(msg: Message):
    user_id = msg.from_user.id
    if users[user_id]["points"] > 0:
        users[user_id]["points"] -= 1
        bot.reply_to(msg, "Here's your note:\n[Physics Notes PDF](https://example.com)", parse_mode="Markdown")
    else:
        bot.reply_to(msg, "You have 0 points.\nUse /refer or /buypoints to get more.")

# Admin-only command to add points
@bot.message_handler(commands=['addpoints'])
def addpoints(msg: Message):
    admin_id = 123456789  # replace with your Telegram user ID
    if msg.from_user.id == admin_id:
        try:
            parts = msg.text.split()
            uid = int(parts[1])
            pts = int(parts[2])
            users[uid]["points"] += pts
            bot.reply_to(msg, f"Added {pts} points to {uid}")
        except:
            bot.reply_to(msg, "Usage: /addpoints user_id amount")

bot.polling()