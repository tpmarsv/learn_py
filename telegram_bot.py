from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import t_info as ti
import logging
import json
import requests
import emoji

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
    search_city = update.message.text
    update.message.reply_text("Ищем в " + search_city + " ..")

    request_str = "http://engine.hotellook.com/api/v2/cache.json?location="+search_city+"&currency=rub&checkIn=2019-07-10&checkOut=2019-07-12&limit=4"
    response_api = requests.get(request_str)
    hotels_j = json.loads(response_api.text)
    
    message_name = hotels_j[0]['hotelName']
    message_low_price = hotels_j[0]['priceFrom']
    update.message.reply_text("Рекомендуем " + message_name + " по цене " + str(message_low_price) + " руб")


if __name__ == "__main__":
    main()
