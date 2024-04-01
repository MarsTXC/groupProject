import firebase_admin
from firebase_admin import credentials, db
import configparser
from telegram import Update
from telegram.ext import CallbackContext

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 初始化 Firebase
cred_object = credentials.Certificate('./firebase.json')
firebase_admin.initialize_app(cred_object, {
    'databaseURL': config['FIREBASE']['URL']
})

class Store():
    def save_recipe(self, update: Update, context: CallbackContext) -> None:
        try:
            Recipe, Country, Flavor, Comment = context.args

            # 构建 Firebase 数据库引用并保存数据
            db.reference(f'{update.message.from_user.id}/{Country}/{Recipe}/flavor').set(Flavor)
            db.reference(f'{update.message.from_user.id}/{Country}/{Recipe}/comment').set(Comment)

            context.bot.send_message(
                chat_id=update.message.from_user.id, text='Recipe has been saved.')
        except Exception as e:
            print(f"Error saving recipe: {e}")
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Usage: /save <Recipe> <Country> <Flavor> <Comment>')

    def get_recipe(self, update: Update, context: CallbackContext) -> None:
        try:
            # 获取并格式化食谱数据
            data = db.reference(f'{update.message.from_user.id}/').get()
            formatted_data = self.format_data(data)

            context.bot.send_message(
                chat_id=update.message.from_user.id, text=formatted_data, parse_mode='Markdown')
        except Exception as e:
            print(f"Error getting recipes: {e}")
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Usage: /list')

    def format_data(self, data):
        if not data:
            return "No recipes found."
        lines = []
        for country, recipes in data.items():
            for recipe, details in recipes.items():
                line = f"*{country} - {recipe}:*\n"
                for key, value in details.items():
                    line += f"  {key.capitalize()}: {value}\n"
                lines.append(line)
        return "\n".join(lines)
