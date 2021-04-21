import re
from flask import Flask, request
import telegram
from credentials import BOT_TOKEN, BOT_USERNAME, URL
from telegram import ParseMode
from random import choice
from threading import Timer

global bot
global TOKEN
TOKEN = BOT_TOKEN
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
ids = [("ori", 138589381), ("or", 1189353214), ("ela", 139725679), ("daniel", 166405779)]


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    t = Timer(60, send_periodically)
    t.start()

    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    print(f"Chat ID: {chat_id}")
    msg_id = update.message.message_id
    print(f"MSG ID: {msg_id}")
    print(f"Update: {update}")
    print(f"Update.message: {update.message}")

    # Telegram understands UTF-8, so encode text for unicode compatibility
    try:
        text = update.message.text.encode('utf-8').decode()
    except (AttributeError):
        text = "/error"
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
        היי! אני משה, הגיימר בוט הידידותי! אני כאן כדי לתת לכם עדכונים על משחקים, לקשקש איתכם, וכמובן לשחק :)
        """
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
        
    elif text == "/tagOri":
        message = "מה קורה"
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id=138589381">ori</a>?', parse_mode='html')
    elif text == "/tagOr":
        message = "לכי לפייתן"
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id=1189353214">or</a>', parse_mode='html')
    elif text == "/tagEla":
        message = "אלה אלה מה קורה לה"
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id=139725679">ela</a>', parse_mode='html')
    elif text == "/tagDaniel":
        message = "תמות יא מנמנמנמנמנמנמניאק"
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id=166405779">daniel</a>', parse_mode='html')

    elif text == "/error":
        message = "An error occured :("
        bot.sendMessage(chat_id=chat_id, text=message)
    elif text == "/tag":
        message = "מה שיחקת לאחרונה?"
        chosen = choice(ids)
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id={chosen[1]}">{chosen[0]}</a>', parse_mode='html')
    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
    

@app.route('/deletewebhook', methods=['GET', 'POST'])
def delet_ewebhook():
    s = bot.deleteWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook deleted"
    else:
        return "webhook deletion failed"


@app.route('/timer', methods=['GET', 'POST'])
def delet_ewebhook():
    s = bot.deleteWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook deleted"
    else:
        return "webhook deletion failed"

 
@app.route('/')
def hello():
    return "Hello World!"


def send_periodically():
    message = "מה שיחקת לאחרונה? ושמת לב ששלחתי לבד בלי תיוג? ^_^"
    chosen = choice(ids)
    bot.sendMessage(chat_id=1001399023645, text=f'{message} <a href="tg://user?id={chosen[1]}">{chosen[0]}</a>', parse_mode='html')


#
if __name__ == '__main__':
    app.run(threaded=True)
