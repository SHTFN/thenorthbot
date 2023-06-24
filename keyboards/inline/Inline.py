from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

RusLangBtn = InlineKeyboardButton('Русский', callback_data='buttonRus')
EngLangBtn = InlineKeyboardButton('English', callback_data='buttonEng')


languages = InlineKeyboardMarkup()
languages.add(RusLangBtn).add(EngLangBtn)