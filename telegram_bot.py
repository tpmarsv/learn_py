from telegram.ext import Updater, CommandHandler

# Настройки прокси
PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080', 'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

# Функция, которая соединяется с платформой Telegram, "тело" нашего бота


def main():
    ‘‘‘
    Комментарий к функции обычно оформляют так
    And better in English
    ’’’
    getroom_bot = Updater("897235175:AAEayBIz7SGML4HTAf8qI9U6ympTbPJ6dGk", request_kwargs=PROXY)
    # токен светить плохо, так как любой другой человек сможет его использовать
    # чтобы этого не произошло, его обычно выносят в отдельный файл, напр мер secrets.py, а потом импортируют
    # сам файл, естественно, добавляют в .gitignore

    dpatch = getroom_bot.dispatcher
    dpatch.add_handler(CommandHandler("start", greet_user))
 
    getroom_bot.start_polling()
    getroom_bot.idle()


def greet_user(bot, update):
    # print(update)
    # хороший тон - удалять все неиспользуемые строки перед коммитом
    # давай добавим ещё обращение по имени или юзернейму? И сделаем 2 Сообщения, одно - приветствие, второе - выбор города
    update.message.reply_text("Привет, хочешь найти комнату на сегодня? Напиши название города где собираешься остановиться")


main()
