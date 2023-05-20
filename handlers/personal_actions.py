from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dispatcher import dp
import config
import re
from bot import BotDB
import logging
import random

logging.basicConfig(level=logging.INFO)


class User(StatesGroup):
    user_number = State()


@dp.message_handler(commands='start', content_types=['text'])
async def send_welcome(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Привет! Это North Smoke.")
    if not BotDB.user_exists(message.from_user.id):
        await message.bot.send_message(message.from_user.id, "Продолжая использование, вы соглашаетесь с "
                                                             "условиями по обработке персональных данных\n"
                                                             "https://youtu.be/dQw4w9WgXcQ")
        await message.answer(text='Введите ваш номер телефона')
        await User.user_number.set()

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Информация').add('Количество баллов')

        await message.bot.send_message(message.from_user.id, "Выберите действие", parse_mode='html',
                                       reply_markup=markup)


@dp.message_handler(state=User.user_number)
async def input_user_number(message: types.Message, state: FSMContext):
    number = message.text
    BotDB.add_user(message.from_user.id, number)
    await message.bot.send_message(message.from_user.id, text=f'Номер телефона {number} успешно добавлен ✅')
    await state.finish()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Информация').add('Количество баллов').add('Тех. поддержка')

    await message.bot.send_message(message.from_user.id, "Выберите действие", parse_mode='html',
                                   reply_markup=markup)
    '''if len(number) == 10 or len(number) == 11:
        BotDB.add_user(message.from_user.id, number)
        await message.bot.send_message(message.from_user.id, text=f'Номер телефона {number} успешно добавлен')
    else:
        await message.bot.send_message(message.from_user.id, text='Введен неправильный номер\nПовторите попытку')
        await send_welcome(types.Message)'''


@dp.message_handler(commands='fuck')
async def fuck(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "тест✅")


@dp.message_handler(text='Информация')
async def info(message: types.Message):
    await message.bot.send_message(message.from_user.id, text="Ваши данные:\n"
                                                              f"Telegram id: {message.from_user.id}\n"
                                                              f"Номер телефона: {BotDB.get_user_phone(message.from_user.id)}")


@dp.message_handler(text='Количество баллов')
async def points(message: types.Message):
    await message.bot.send_message(message.from_user.id,
                                   text=f"Ваше количество баллов: {BotDB.get_points(message.from_user.id)}")


@dp.message_handler(text='Количество баллов')
async def points(message: types.Message):
    await message.bot.send_message(message)

    # @dp.message_handler(content_types=['text'])
    '''@dp.message_handler(commands='testtest')
    async def info(message: types.Message):
        await message.bot.send_message(message.from_user.id, "Привет! Это North Smoke.")
        await message.bot.send_message(message.from_user.id, "Выберите действие")
        if message.chat.type == 'private':
            if message.text == 'Информация':
                message.bot.send_message(message.chat.id, str(random.randint(0, 100)))
            elif message.text == 'Количество баллов':
                message.bot.send_message(message.chat.id, 'баллы')'''

    '''@dp.callback_query_handler(lambda call: True)
    def callback(call):
        if call.message:
            if call.data == 'information':
                bot.send_message(call.message.chat.id, 'info')
            elif call.data == 'points':
                bot.send_message(call.message.chat.id, 'points')'''