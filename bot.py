from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import configparser
import logging
import requests
from store import Store


def equiped_chatgpt(update: Update, context: CallbackContext) -> None:
    global chatgpt
    try:
        reply_message = chatgpt.submit(update.message.text)
        logging.info("Update: " + str(update))
        logging.info("context :" + str(context))
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except Exception as e:
        logging.error(
            "An error occurred while processing the message: %s", str(e))

# def save_recipe(update: Update, context: CallbackContext) -> None:
#     print('')  

# def get_recipe(update: Update, context: CallbackContext) -> None:
#     print('')

def getRecipe(update: Update, context: CallbackContext) -> None:
    if (context.args == []):
        cuisine = 'unspecified'
    else:
        cuisine = context.args[0]

    global chatgpt
    reply_message = chatgpt.list_recipe(cuisine)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)

# def error_handler(update, context):
#     """Log Errors caused by Updates."""
#     logging.error("Exception while handling an update:",
#                   exc_info=context.error)


class HKBU_GPT():
    def __init__(self, config='./config.ini'):
        if type(config) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config)
        elif type(config) == configparser.ConfigParser:
            self.config = config

    def submit(self, message):
        """submit 

        Args:
            message (_type_): _description_

        Returns:
            _type_: _description_
        """

        conversation = [{"role": "user", "content": message}]
        url = (self.config['CHATGPT']['BASICURL']) + "/deployments/" + (self.config['CHATGPT']
                                                                        ['MODELNAME']) + "/chat/completions/?api-version=" + (self.config['CHATGPT']['APIVERSION'])
        headers = {'Content-Type': 'application/json',
                   'api-key': (self.config['CHATGPT']['ACCESS_TOKEN'])}
        payload = {'messages': conversation}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response
        
    def list_recipe(self, message):
        """list recipe by ChatGPT

        Args:
            message (_type_): _description_

        Returns:
            _type_: _description_
        """

        conversation = [
            {'role': 'system',
             'content': "You are a recipe recommendation bot. You will use the following format: -cuisine:, -country:, -taste:, -duration:. Each item should use blank line to separate.  User will input a cuisine, and you will list 4 recipes about this cuisine. If user input unspecified, it means you will recommend 4 different cuisine's recipes."},
            {"role": "user", "content": message}
        ]
        url = (self.config['CHATGPT']['BASICURL']) + "/deployments/" + (self.config['CHATGPT']
                                                                        ['MODELNAME']) + "/chat/completions/?api-version=" + (self.config['CHATGPT']['APIVERSION'])
        headers = {'Content-Type': 'application/json',
                   'api-key': (self.config['CHATGPT']['ACCESS_TOKEN'])}
        payload = {'messages': conversation}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.

    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(config['TELEGRAM']['TELEGRAM_TOKEN'])

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    global chatgpt
    chatgpt = HKBU_GPT()
    chatgpt_handler = MessageHandler(
        Filters.text & (~Filters.command), equiped_chatgpt)
    updater.dispatcher.add_handler(chatgpt_handler)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler("recipe", getRecipe))
    st = Store()
    updater.dispatcher.add_handler(CommandHandler("save", st.save_recipe))
    updater.dispatcher.add_handler(CommandHandler("list", st.get_recipe))


    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
