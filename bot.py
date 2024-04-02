from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import configparser
import logging
import requests
from store import Store

# 定义处理普通文本消息的函数，利用 ChatGPT 生成回复
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

# 启动命令的处理函数，向用户发送欢迎信息
def start(update: Update, context: CallbackContext) -> None:
    welcome_message = "Welcome to use this Bot! Use /recipe to view the recipe, use /save to save the recipe, and use /list to list all the recipes."
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

# 关闭 Bot 的命令处理函数（仅供开发者使用）
def shutdown(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == 6882913651:  # 请替换为你的 Telegram 用户 ID
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bot shutting down...")
        update.stop()
        update.is_idle = False
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Permission denied")

# 根据用户输入的菜系，获取食谱的处理函数
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

class HKBU_GPT():
    # 初始化 ChatGPT 相关配置
    def __init__(self, config='./config.ini'):
        if type(config) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config)
        elif type(config) == configparser.ConfigParser:
            self.config = config

    # 提交消息到 ChatGPT 并获取回复
    def submit(self, message):
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
        
    # 根据用户输入的菜系，获取 ChatGPT 生成的食谱列表
    def list_recipe(self, message):
        conversation = [
            {'role': 'system',
             'content': "You are a recipe recommendation bot. You will use the following format: -cuisine:, -country:, -taste:, -duration:. Each item should use a blank line to separate. User will input a cuisine, and you will list 4 recipes about this cuisine. If user inputs 'unspecified', it means you will recommend 4 different cuisine's recipes."},
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
    # 启动 Bot 并设置命令处理器
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(config['TELEGRAM']['TELEGRAM_TOKEN'], use_context=True)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    global chatgpt
    chatgpt = HKBU_GPT()
    chatgpt_handler = MessageHandler(
        Filters.text & (~Filters.command), equiped_chatgpt)
    updater.dispatcher.add_handler(chatgpt_handler)

    # 注册命令处理器
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("shutdown", shutdown))
    updater.dispatcher.add_handler(CommandHandler("recipe", getRecipe))

    st = Store()  # 实例化 Store 类来处理食谱保存和查询
    updater.dispatcher.add_handler(CommandHandler("save", st.save_recipe))
    updater.dispatcher.add_handler(CommandHandler("list", st.get_recipe))

    updater.start_polling()  # 开始轮询
    updater.idle()  # Bot 进入待机状态

if __name__ == '__main__':
    main()
