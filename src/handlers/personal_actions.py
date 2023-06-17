from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dispatcher import dp
from main import BotDB
from keyboards.default.Keyboards import main, main_admin, admin_panel
import config

class User(StatesGroup):
    user_number = State()

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Привет! Это North Smoke.")
    if not BotDB.user_exists(message.from_user.id):
        await message.bot.send_message(message.from_user.id, "Продолжая использование, вы соглашаетесь с "
                                                             "условиями по обработке персональных данных\n"
                                                             "https://youtu.be/dQw4w9WgXcQ")
        await message.answer(text='Введите ваш номер телефона')
        await User.user_number.set()
    else:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать. Выберите действие', reply_markup=main)
        if message.from_user.id in config.ADMIN_ID:
            await message.answer(f'Вы авторизованы как администратор', reply_markup=main_admin)


@dp.message_handler(state=User.user_number)
async def input_user_number(message: types.Message, state: FSMContext):
    number = message.text
    true_number = ''
    for i in number:
        if i in '0123456789':
            true_number += i
    BotDB.add_user(message.from_user.id, true_number)
    await message.answer(f'Номер телефона {true_number} успешно добавлен ✅')
    await state.finish()
    if message.from_user.id in config.ADMIN_ID:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать. Выберите действие',
                             reply_markup=main_admin)
    else:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать. Выберите действие',
                             reply_markup=main)

@dp.message_handler(text='Информация')
async def info(message: types.Message):
    await message.bot.send_message(message.from_user.id, text="Ваши данные:\n"
                                                              f"Telegram id: {message.from_user.id}\n"
                                                              f"Номер телефона: {BotDB.get_user_phone(message.from_user.id)}")


@dp.message_handler(text='Количество баллов')
async def points(message: types.Message):
    await message.bot.send_message(message.from_user.id,
                                   text=f"Ваше количество баллов: {BotDB.get_points(message.from_user.id)}")

@dp.message_handler(text='Админ-панель')
async def points(message: types.Message):
    if message.from_user.id in config.ADMIN_ID:
        await message.answer(f'Вы вошли в админ-панель ✅', reply_markup=admin_panel)
    else:
        await message.answer(f'Сообщение не распознано ❌')

@dp.message_handler(text='Поддержка')
async def contacts(message: types.Message):
    await message.answer(f'Для обращения в служду поддержки напишите сюда: \n@thenorthsmokehelp_bot\n'
                         f'Или напишите на почту:\n<code>the-north-smoke-bot-help@mail.ru</code>')

@dp.message_handler(text='Создать рассылку')
async def create_mailing_list(message: types.Message):
    if message.from_user.id in config.ADMIN_ID:
        await message.answer(f'Для создания рассылки введите команду /sendall *Ваш текст*')
    else:
        await message.answer(f'Сообщение не распознано ❌')

@dp.message_handler(commands='sendall')
async def sendall(message: types.Message):
    if message.from_user.id in config.ADMIN_ID:
        if len(message.text) <= 9:
            await message.answer('Ошибка: вы не ввели рассылаемый текст')
        else:
            text = message.text[9:]
            users = BotDB.get_users()
            for row in users:
                try:
                    await message.bot.send_message(row[0], text)
                except:
                    await message.bot.send_message('Ошибка ❌')
            await message.answer(f'Рассылка завершена ✅')
    else:
        await message.answer(f'Сообщение не распознано ❌')

@dp.message_handler(commands="getchatid")
async def cmd_test1(message: types.Message):
    await message.reply("Добро пожаловать в бота")
    chat_id = message.chat.id
    print('id', chat_id)

@dp.message_handler(commands='support')
async def call_support(message: types.Message):
    pass



@dp.message_handler()
async def pass_func(message: types.Message):
    if message.from_user.id in config.ADMIN_ID:
        await message.answer(f'Сообщение не распознано ❌', reply_markup=main_admin)
    else:
        await message.answer(f'Сообщение не распознано ❌', reply_markup=main)
