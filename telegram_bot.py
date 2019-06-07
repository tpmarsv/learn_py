from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import t_info as ti
import logging

# Настройки прокси
PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080', 'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='telegram_bot.log'
                    )


def main():
    '''
    Main bot listener and dispatcher
    '''
    tcp_logger = logging.getLogger('tcplogger')
    try:
        getroom_bot = Updater(ti.t_str, request_kwargs=PROXY)
    except (ConnectionError, TimeoutError):
        tcp_logger.warning("Protocol problem: %s", "ошибка установки соединения")
    finally:
        tcp_logger.warning("Protocol problem: %s", "ошибка установки соединения с telegram-сервером")

    dpatch = getroom_bot.dispatcher
    dpatch.add_handler(CommandHandler("start", greet_user))
    dpatch.add_handler(MessageHandler(Filters.text, bestrooms_byCity))

    getroom_bot.start_polling()
    getroom_bot.idle()


def greet_user(bot, update):
    '''
    Greet and request city
    '''

    chat_username = update.message.chat.username
    update.message.reply_text("Привет, " + chat_username + ", хочешь найти комнату на сегодня?")
    update.message.reply_text("Напиши название города, где собираешься остановиться")


def bestrooms_byCity(bot, update):
    '''
    Search by city
    '''
    update.message.reply_text("Ищем в " + update.message.text + " ..")


if __name__ == "__main__":
    main()
