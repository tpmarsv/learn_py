from telegram.ext import Updater, CommandHandler

# Настройки прокси
PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080', 'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

# Функция, которая соединяется с платформой Telegram, "тело" нашего бота


def main():
    getroom_bot = Updater("897235175:AAEayBIz7SGML4HTAf8qI9U6ympTbPJ6dGk", request_kwargs=PROXY)

    dpatch = getroom_bot.dispatcher
    dpatch.add_handler(CommandHandler("start", greet_user))
 
    getroom_bot.start_polling()
    getroom_bot.idle()


def greet_user(bot, update):
    # print(update)
    update.message.reply_text("Привет, хочешь найти комнату на сегодня? Напиши название города где собираешься остановиться")


main()
