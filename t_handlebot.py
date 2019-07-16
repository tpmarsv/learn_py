from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import json
import requests
from emoji import emojize
from datetime import datetime, timedelta
from funcy import cache


def greet_user(bot, update):
    '''
    Greet and request city
    '''

    chat_username = update.message.chat.username
    emoj_location = emojize('📍', use_aliases=True)
    emoj_help = emojize('ℹ️', use_aliases=True)
    emoj_ru = emojize('🇷🇺', use_aliases=True)
    emoj_gb = emojize('🇬🇧', use_aliases=True)

    menu_kb = []
    menu_kb.append([KeyboardButton(emoj_location + 'Найти рядом', request_location=True)])
    menu_kb.append([KeyboardButton(emoj_help, callback_data='/help'), KeyboardButton(emoj_ru, callback_data='ru'), KeyboardButton(emoj_gb, callback_data='gb')])

    update.message.reply_text("Привет, " + chat_username + ", хочешь найти комнату на сегодня?")
    update.message.reply_text("Напиши название города, где собираешься остановиться или нажми " + emoj_location + " Найти рядом", reply_markup=ReplyKeyboardMarkup(menu_kb, resize_keyboard=True, one_time_keyboard=True))


def bestrooms_byCity(bot, update):
    '''
    Search by city and response to user best rooms by given params
    '''
    search_city = update.message.text
    update.message.reply_text("Ищем в " + search_city + " ..")

    today_date = datetime.now()
    next_day_date = today_date + timedelta(days=1)
    checkin_date = today_date.strftime('%Y-%m-%d')
    checkout_date = next_day_date.strftime('%Y-%m-%d')

    hotels_j_s = get_rooms_byCity(search_city)

    for i in range(0, 3):
        hotel_message_name = hotels_j_s[i]['hotelName']
        message_low_price = hotels_j_s[i]['priceFrom']
        hotel_id = str(hotels_j_s[i]['hotelId'])
        book_url = 'https://search.hotellook.com/hotels?destination=' + hotel_message_name + '&checkIn=' + checkin_date + '&checkOut=' + checkout_date + '&marker=direct&children=&adults=1&language=ru&currency=rub&hotelId=' + hotel_id
        keyboard = [[InlineKeyboardButton('Бронь', url=book_url, callback_data='book in ' + hotel_id), InlineKeyboardButton('Детали', url=book_url + '#mds%3Dhotels_map', callback_data='details for ' + hotel_id)]]
        update.message.reply_text("Рекомендуем " + hotel_message_name + " по цене от " + str(message_low_price) + " руб")
        update.message.reply_text("Нравится?", reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True))


@cache(150)
def get_rooms_byCity(search_city):
    '''
    Request API and use sort to return sort list of hotels (not rooms)
    '''
    today_date = datetime.now()
    today_date = today_date.strftime('%Y-%m-%d')

    request_str = "http://engine.hotellook.com/api/v2/cache.json?location="+search_city+"&currency=rub&checkIn=" + today_date + "&checkOut=" + today_date + "&limit=10"
    response_api = requests.get(request_str)
    hotels_j = json.loads(response_api.text)
    hotels_j_s = sort_list_of_dict(hotels_j, 'priceFrom')

    return hotels_j_s


def sort_list_of_dict(ld_for_sort, sort_by_item):
    sort_l = sorted(ld_for_sort, key=lambda x: x[sort_by_item])
    return sort_l


def button_cl(bot, update):
    '''
    Inline button choose return actions: book room or details about rooms
    '''
    query = update.callback_query
    if ('book' in query.data):
        query.edit_message_text(text="Переходим к бронированию " + query.data)
    elif ('details' in query.data):
        query.edit_message_text(text="Переходим к номерам отеля " + query.data)
    elif ('help' in query.data):
        update.message.reply_text('Бот поможет найти комнату сегодня\n Поиск покажет ближайшие недорогие отели по местоположению (кнопка ) или введенному вами названию города')


def help_info(bot, update):
    '''
    Send help information
    '''
    update.message.reply_text('Бот @getroom_bot поможет найти комнату сегодня\n Поиск покажет ближайшие недорогие отели по местоположению (кнопка ) или введенному вами названию города')
