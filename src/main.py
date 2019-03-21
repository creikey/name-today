#!/usr/bin/env python

import coloredlogs, logging
import schedule
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler

from days import Day, get_today, get_word, get_announcement

coloredlogs.install(level="DEBUG")

DAILY_UPDATE_TIME = "07:00"
TOKEN_FILE_NAME = ".token"
HELP_TEXT = f"""\
/start  start
/help   show this message
/today  show today's word
/subscribe  subscribe to daily updates in this chat at {DAILY_UPDATE_TIME}
/unsubscribe    unsubscribe from daily updates
/status state subscription status
"""

updater = None
cur_day_announcement = get_announcement()
subscribed_chats = []

with open(TOKEN_FILE_NAME, "r") as tf:
    telegram_token = tf.readline().rstrip()
    logging.info(f"Using token {telegram_token}...")
    updater = Updater(token=telegram_token)
assert updater

dispatcher = updater.dispatcher


def update_cur_day_announcement():
    global cur_day_announcement
    cur_day_announcement = get_announcement()


def announce_to_all():
    global subscribed_chats
    for id in subscribed_chats:
        updater.bot.send_message(
            chat_id=id, text=f"YOOOOOOO! IT'S {cur_day_announcement}"
        )


def start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I can tell you what day it is! Type /help to see what I can do",
    )


def help(bot: Bot, update: Update):
    update.message.reply_text(HELP_TEXT)


def today(bot: Bot, update: Update):
    logging.debug(f"Sending {cur_day_announcement} to {update.message.chat_id}...")
    update.message.reply_text(cur_day_announcement)


def subscribe(bot: Bot, update: Update):
    subscribed_chats.append(update.message.chat_id)
    update.message.reply_text(f"Subscribing for messages at {DAILY_UPDATE_TIME}...")


def unsubscribe(bot: Bot, update: Update):
    subscribed_chats.remove(update.message.chat_id)
    update.message.reply_text("Unsubscribing from messages...")


def status(bot: Bot, update: Update):
    if update.message.chat_id in subscribed_chats:
        update.message.reply_text(
            f"You are currently subscribed for messages at {DAILY_UPDATE_TIME}"
        )
    else:
        update.message.reply_text("You are currently unsubscribed")


commands = ["start", "help", "today", "subscribe", "unsubscribe", "status"]
for c in commands:
    dispatcher.add_handler(CommandHandler(c, locals()[c]))

schedule.every().day.at("00:00").do(update_cur_day_announcement)
schedule.every().day.at(DAILY_UPDATE_TIME).do(announce_to_all)

updater.start_polling()

while True:
    schedule.run_pending()
    time.sleep(1)
