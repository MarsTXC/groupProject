from flask import Flask, request
import bot  # 导入Telegram机器人逻辑

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World from Flask!"

if __name__ == '__main__':
    bot.run_bot()  # 启动Telegram机器人
    app.run(debug=True)
