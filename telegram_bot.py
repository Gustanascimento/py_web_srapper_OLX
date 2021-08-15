import telegram
from telegram_info import *  # .gitignore telegram_info.py

bot = telegram.Bot(token=token)


def telegram_bot_send_message(titulo, data_postagem, preco, url):
    message = ''
    message += '* ‼ Novo anúncio detectado! ‼*'
    message += '\n\n'
    message += '*Título: *'
    message += titulo
    message += '\n\n'
    message += '*Data da postagem:* '
    message += data_postagem
    message += '\n\n'
    message += '*Preço: *'
    message += preco
    message += '\n\n'
    message += '*Link: *'
    message += url
    message += '\n\n 😎'

    bot.send_message(text=message, chat_id=chat_id, parse_mode=telegram.ParseMode.MARKDOWN)
    print(f'Telegram Bot Says: "Message Sent!"')
