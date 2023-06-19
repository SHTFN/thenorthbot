from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dispatcher import dp
from main import BotDB
from keyboards.default.Keyboards import main, main_admin, admin_panel
from functions.Functions import check_admin


class User(StatesGroup):
    user_number = State()
    text_of_the_appeal = State()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Привет! Это North Smoke.")
    if not BotDB.user_exists(message.from_user.id):
        await message.bot.send_message(message.from_user.id, "Продолжая использование, вы соглашаетесь с "
                                                             "условиями по обработке персональных данных\n"
                                                             "https://youtu.be/dQw4w9WgXcQ")
        await message.answer('Введите ваш номер телефона')
        await User.user_number.set()
    else:
        if check_admin(message.from_user.id):
            await message.answer(f'Вы авторизованы как администратор', reply_markup=main_admin)
        else:
            await message.answer(f'{message.from_user.first_name}, добро пожаловать. Выберите действие',
                                 reply_markup=main)


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
    if check_admin(message.from_user.id):
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
    if check_admin(message.from_user.id):
        await message.answer(f'Вы вошли в админ-панель ✅', reply_markup=admin_panel)
    else:
        await message.answer(f'Сообщение не распознано ❌')


@dp.message_handler(text='Создать рассылку')
async def create_mailing_list(message: types.Message):
    if check_admin(message.from_user.id):
        await message.answer(f'Для создания рассылки введите команду /sendall *Ваш текст*')
    else:
        await message.answer(f'Сообщение не распознано ❌')


@dp.message_handler(commands='sendall')
async def sendall(message: types.Message):
    if check_admin(message.from_user.id):
        if len(message.text) <= 9:
            await message.answer('Ошибка: вы не ввели рассылаемый текст')
        else:
            text = message.text[9:]
            users = BotDB.get_users()
            for row in users:
                try:
                    await message.answer(row[0], text)
                except ValueError:
                    await message.answer('Ошибка ❌')
            await message.answer(f'Рассылка завершена ✅')
    else:
        await message.answer(f'Сообщение не распознано ❌')


@dp.message_handler(commands="getchatid")
async def cmd_test1(message: types.Message):
    await message.bot.send_message(message.from_user.id, message.chat.id)


@dp.message_handler(text='Поддержка')
async def forward_message(message: types.Message):
    await message.answer('Опишите вашу проблему', reply_markup=types.ReplyKeyboardRemove())
    await User.text_of_the_appeal.set()


@dp.message_handler(state=User.text_of_the_appeal)
async def send_forward_message(message: types.Message, state: FSMContext):
    await message.bot.send_message(-995941442, '📫 | Новое обращение')
    await message.bot.forward_message(-995941442, message.from_user.id, message.message_id)
    await message.bot.send_message(-995941442,
                                   f'ID пользователя {message.from_user.first_name}: {message.from_user.id}')
    await state.finish()
    # await message.answer('📨 | Сообщение отправлено в поддержку')

    if check_admin(message.from_user.id):
        await message.answer('📨 | Сообщение отправлено в поддержку', reply_markup=main_admin)
    else:
        await message.answer('📨 | Сообщение отправлено в поддержку', reply_markup=main)


@dp.message_handler(commands='responsetouser')
async def response_to_user(message: types.Message):
    temp = message.text.split()
    text = ' '.join(temp[2:])
    await message.bot.send_message(temp[1], '📫 | Новое уведомление!\n'
                                            'Ответ от техподдержки:\n'
                                            '\n'
                                            f'<code>{text}</code>')


@dp.message_handler(text='Отмена')
async def cancel(message: types.Message):
    if check_admin(message.from_user.id):
        await message.answer(f'Выберите действие', reply_markup=main_admin)
    else:
        await message.answer(f'Выберите действие', reply_markup=main)


@dp.message_handler()
async def pass_func(message: types.Message):
    if check_admin(message.from_user.id):
        await message.answer(f'Сообщение не распознано ❌', reply_markup=main_admin)
    else:
        await message.answer(f'Сообщение не распознано ❌', reply_markup=main)
