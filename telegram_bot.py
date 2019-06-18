from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import t_info as ti
import logging
import json
import requests
import emoji
from datetime import datetime

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

    today_date = datetime.now()
    today_date = today_date.strftime('%Y-%m-%d')

    request_str = "http://engine.hotellook.com/api/v2/cache.json?location="+search_city+"&currency=rub&checkIn=" + today_date + "&checkOut=" + today_date + "&limit=10"
    response_api = requests.get(request_str)
    hotels_j = json.loads(response_api.text)
    hotels_j_s = sort_list_of_dict(hotels_j, 'priceFrom')

    for i in range(0, 3):
        message_name = hotels_j_s[i]['hotelName']
        message_low_price = hotels_j_s[i]['priceFrom']
        update.message.reply_text("Рекомендуем " + message_name + " по цене " + str(message_low_price) + " руб")


def sort_list_of_dict(ld_for_sort, sort_by_item):
    sort_l = sorted(ld_for_sort, key=lambda x: x[sort_by_item])
    return sort_l


if __name__ == "__main__":
    main()
