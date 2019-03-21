import coloredlogs, logging
import schedule
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler

from days import Day, get_today, get_word, get_announcement

coloredlogs.install(level="DEBUG")

TOKEN_FILE_NAME = ".token"
HELP_TEXT = """\
/start  start
/help   show this message
/today  show today's word
"""

updater = None
cur_day_announcement = get_announcement()

with open(TOKEN_FILE_NAME, "r") as tf:
    telegram_token = tf.readline().rstrip()
    logging.info(f"Using token {telegram_token}...")
    updater = Updater(token=telegram_token)
assert updater

dispatcher = updater.dispatcher


def update_cur_day_announcement():
    global cur_day_announcement
    cur_day_announcement = get_announcement()


def start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I can tell you what day it is! Type /help to see what I can do",
    )


def help(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text=HELP_TEXT)


def today(bot: Bot, update: Update):
    logging.debug(f"Sending {cur_day_announcement} to {update.message.chat_id}...")
    bot.send_message(chat_id=update.message.chat_id, text=cur_day_announcement)


commands = ["start", "help", "today"]
for c in commands:
    dispatcher.add_handler(CommandHandler(c, locals()[c]))

schedule.every().day.at("00:00").do(update_cur_day_announcement)

updater.start_polling()

while True:
    schedule.run_pending()
    time.sleep(1)
