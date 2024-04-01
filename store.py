import firebase_admin
from firebase_admin import db
import configparser
import json
from telegram import ParseMode, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)

config = configparser.ConfigParser()
config.read('config.ini')

cred_object = firebase_admin.credentials.Certificate('./firebase.json')
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': config['FIREBASE']['URL']
})

class Store():
    def __init__(self) -> None:
        # config = configparser.ConfigParser()
        # config.read('config.ini')
        # cred_object = firebase_admin.credentials.Certificate('./firebase.json')
        # default_app = firebase_admin.initialize_app(cred_object, {
        #     'databaseURL': config['FIREBASE']['URL']
        # })
        pass
    
    def save_recipe(self, update: Update, context: CallbackContext) -> None:
        try:
            Recipe, Country, Flavor, Comment = context.args

            set_falvor = db.reference(
                f'{update.message.from_user.id}/{Country}/{Recipe}/flavor')
            set_comment = db.reference(
                f'{update.message.from_user.id}/{Country}/{Recipe}/comment')
            set_falvor.set(Flavor)
            set_comment.set(Comment)

            context.bot.send_message(
                chat_id=update.message.from_user.id, text='Recipe has been saved.')
        except:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Usage: /save <Recipe> <Country> <flavor> <Comment>')

    def get_recipe(self, update: Update, context: CallbackContext) -> None:
        try:
            lists = db.reference(f'{update.message.from_user.id}/')
            data = lists.get()

            context.bot.send_message(
                chat_id=update.message.from_user.id, text=data)
        except:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Usage: /list')
