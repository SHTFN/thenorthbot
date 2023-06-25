from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

RusLangBtn = InlineKeyboardButton('Русский', callback_data='buttonRus')
EngLangBtn = InlineKeyboardButton('English', callback_data='buttonEng')

category_1 = InlineKeyboardButton('Категория 1', callback_data='ctg1')
category_2 = InlineKeyboardButton('Категория 2', callback_data='ctg2')
category_3 = InlineKeyboardButton('Категория 3', callback_data='ctg3')

languages = InlineKeyboardMarkup()
languages.add(RusLangBtn).add(EngLangBtn)

catalog = InlineKeyboardMarkup()
catalog.add(category_1).add(category_2).add(category_3)

product_1_1 = InlineKeyboardButton('Товар 1', callback_data='product1_1')
product_1_2 = InlineKeyboardButton('Товар 2', callback_data='product1_2')
back_1 = InlineKeyboardButton('Назад', callback_data='back1')

btn_back_1_1 = InlineKeyboardButton('Назад', callback_data='back_1_1')
back_1_1 = InlineKeyboardMarkup.add(btn_back_1_1)
catalog_category_1 = InlineKeyboardMarkup()
catalog_category_1.row(product_1_1, product_1_2).add(back_1)