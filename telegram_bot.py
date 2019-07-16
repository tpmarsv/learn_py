import t_dispatcher as t_botDp


t_botDp.logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=t_botDp.logging.INFO,
                    filename='telegram_bot.log'
                    )


def main():
    '''
    Main bot listener and dispatcher
    '''
    t_botDp.set_bot_dispatchers()


if __name__ == "__main__":
    main()
