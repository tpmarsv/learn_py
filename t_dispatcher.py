from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler
import t_handlebot as thb
import t_info as ti
import logging


def set_bot_dispatchers():
    '''
    Main bot listener and dispatcher
    '''
    tcp_logger = logging.getLogger('tcplogger')
    try:
        getroom_bot = Updater(ti.t_str, request_kwargs=ti.PROXY)
    except (ConnectionError, TimeoutError):
        tcp_logger.warning("Protocol problem: %s", "ошибка установки соединения")
    finally:
        tcp_logger.warning("Protocol problem: %s", "ошибка установки соединения с telegram-сервером")

    dpatch = getroom_bot.dispatcher
    dpatch.add_handler(CommandHandler("start", thb.greet_user))
    dpatch.add_handler(CommandHandler("help", thb.help_info))
    dpatch.add_handler(CallbackQueryHandler(thb.button_cl))
    dpatch.add_handler(MessageHandler(Filters.text, thb.bestrooms_byCity))

    getroom_bot.start_polling()
    getroom_bot.idle()
