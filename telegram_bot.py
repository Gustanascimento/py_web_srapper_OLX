import telegram
from telegram_info import *  # .gitignore telegram_info.py

bot = telegram.Bot(token=token)


def telegram_bot_send_message(titulo, data_postagem, preco, url):
    message = ''
    message += 'Novo anúncio detectado!'
    message += '\n'
    message += 'Título: '
    message += titulo
    message += '\n'
    message += 'Data da postagem: '
    message += data_postagem
    message += '\n'
    message += 'Preço: '
    message += preco
    message += '\n'
    message += 'Link: '
    message += url

    bot.send_message(text=message, chat_id=chat_id)
    print(f'Telegram Bot Says: "Message Sent!"')
