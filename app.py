import re
from flask import Flask, request
import telegram
# from credentials import BOT_TOKEN, BOT_USERNAME, URL
from random import choice
from threading import Timer
from datetime import time
from telegram.ext import JobQueue, Updater
import schedule
from threading import Thread
from time import sleep
import os
from random import choice

global bot
global TOKEN
TOKEN = os.environ["BOT_TOKEN"]
BOT_USERNAME = os.environ["BOT_USERNAME"]
URL = os.environ["URL"]
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
ids = [("ori", 138589381), ("or", 1189353214), ("ela", 139725679), ("daniel", 166405779)]


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    #t = Timer(60, send_periodically)
    #t.start()

    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    updater = Updater(TOKEN, use_context=True)
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
        if update.message.new_chat_members:
            text = "/Welcome!"
        elif update.message.left_chat_member:
            text = "/Leaving"
        else:
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
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id=1189353214">or</a>!', parse_mode='html')
    elif text == "/tagEla":
        message = "אלה אלה מה קורה לה"
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id=139725679">ela</a>', parse_mode='html')
    elif text == "/tagDaniel":
        message = "תמות יא מנמנמנמנמנמנמניאק"
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id=166405779">daniel</a>', parse_mode='html')
    elif text == '/Welcome!':
        try:
            message = f'Welcome {update.message["new_chat_members"][0]["first_name"]}'
        except IndexError:
            message = f'Welcome stranger'
        bot.send_message(chat_id=chat_id, text=message)
        bot.sendAnimation(chat_id=chat_id, animation=get_random_gif())
    elif text == '/Leaving':
        message = "why did they leave us? :("
        bot.sendMessage(chat_id=chat_id, text=message)
    elif text == "/error":
        message = "An error occured :("
        bot.sendMessage(chat_id=chat_id, text=message)
    elif text == "/tag":
        message = "מה שיחקת לאחרונה?"
        chosen = choice(ids)
        bot.sendMessage(chat_id=chat_id, text=f'{message} <a href="tg://user?id={chosen[1]}">{chosen[0]}</a>', parse_mode='html')
    elif text == "/reminder":
        q = JobQueue()
        reminder(update, updater)
    elif text == '/in_except':
        bot.sendMessage(chat_id=chat_id, text='in except')
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

 
@app.route('/')
def hello():
    return "Hello World!"


def send_periodically():
    message = "מה שיחקת לאחרונה? ושמת לב ששלחתי לבד בלי תיוג? ^_^"
    chosen = choice(ids)
    bot.sendMessage(chat_id=1001399023645, text=f'{message} <a href="tg://user?id={chosen[1]}">{chosen[0]}</a>', parse_mode='html')


def callback_alarm(context: telegram.ext.CallbackContext):
  bot.send_message(chat_id=1001399023645, text='Hi, This is a daily reminder')


def reminder(update, context):
   bot.send_message(chat_id = update.effective_chat.id , text='Daily reminder has been set! You\'ll get notified at 8 AM daily')
   context.job_queue.run_daily(callback_alarm, context=update.message.chat_id,days=(0, 1, 2, 3, 4, 5, 6),time = time(hour = 10, minute = 10, second = 10))


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    bot.send_animation(chat_id=-1001399023645, animation="https://i.gifer.com/7Ijg.mp4")
    bot.sendMessage(chat_id=-1001399023645, text="Hello!")
    print("hi from send_message")
    return "success sending message"


def schedule_checker():
    while True:
        print("in schedule_checker")
        schedule.run_pending()
        sleep(1)


def function_to_run():
    bot.sendMessage(chat_id=1001399023645, text="Hello!")
    print("hi")
    #return bot.send_message(some_id, "This is a message to send.")

def get_random_gif():
    with open('gifs.txt', 'r') as f:
        lines = f.readlines()
        return choice(lines)
#testing
if __name__ == '__main__':
    # Create the job in schedule.
    #schedule.every().minute.do(function_to_run)
    #schedule.every().saturday.at("07:00").do(function_to_run)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    #Thread(target=schedule_checker).start() 
    app.run(threaded=True)
    #
