#import pip
# pip.main(['install', 'aiogram', 'python-dotenv])
# from keep_alive import keep_alive
from aiogram import executor
from dispatcher import dp
import handlers

from db import BotDB

BotDB = BotDB('accounts.db')

if __name__ == "__main__":
    # keep_alive()
    executor.start_polling(dp, skip_updates=True)
