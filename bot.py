from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import configparser
import logging
import requests


def start(update: Update, _: CallbackContext) -> None:
    """Sends a message when the command /start is issued."""
    update.message.reply_text('Hi! I am MarsTan, a ChatGPT-powered Telegram Bot.')

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
    
def equiped_chatgpt(update, context):
    global chatgpt
    try:
        reply_message = chatgpt.submit(update.message.text)
        logging.info("Update: " +str(update))
        logging.info("context :" + str(context))
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
    except Exception as e:
        logging.error("An error occurred while processing the message: %s", str(e))

def error_handler(update, context):
    """Log Errors caused by Updates."""
    logging.error("Exception while handling an update:", exc_info=context.error)

class HKBU_GPT():
    def __init__(self, config='./config.ini'):
        if type(config) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config)
        elif type(config) == configparser.ConfigParser:
            self.config = config
        #pass
    
    def submit(self, message):
        conversation = [{"role": "user", "content": message}]
        url = (os.environ['BASICURL']) + "/deployments/" + (os.environ['MODELNAME']) + "/chat/completions/?api-version=" + (os.environ['APIVERSION'])
        headers = { 'Content-Type': 'application/json', 'api-key': (os.environ['chatGPT_access_token']) }
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response
        
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    global chatgpt
    chatgpt = HKBU_GPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),equiped_chatgpt)
    updater.dispatcher.add_handler(chatgpt_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
