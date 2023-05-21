#import pip
#pip.main(['install', 'aiogram'])
from aiogram import executor
from src.dispatcher import dp

from src.db import BotDB
BotDB = BotDB('accounts.db')

if __name__ == "__main__":
  print('hello')
  #keep_alive()
  executor.start_polling(dp, skip_updates=True)