from dotenv import load_dotenv
from os.path import exists
from os import getenv
from pyrogram import Client


load_dotenv()


def login():
    if exists('pytuber_bot.session'):
        return Client('pytuber_bot')
    return Client(
        'pytuber_bot',
        api_id=int(getenv('API_ID')),
        api_hash=getenv('API_HASH'),
        bot_token=getenv('BOT_TOKEN')
    )