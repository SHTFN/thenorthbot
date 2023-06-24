from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import messages
from dispatcher import dp
from main import BotDB
from keyboards.default.Keyboards import ReplyKeyboadrs as rk
from keyboards.inline.Inline import languages
from functions.Functions import check_admin


class User(StatesGroup):
    user_number = State()
    new_user_number = State()
    text_of_the_appeal = State()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        await message.bot.send_message(message.from_user.id,
                                       'Привет! Это North Smoke.')
        await message.bot.send_message(message.from_user.id,
                                       'Продолжая использование, вы соглашаетесь с '
                                       'условиями по обработке персональных данных\n'
                                       'https://youtu.be/dQw4w9WgXcQ')
        await message.answer('Введите ваш номер телефона')
        await User.user_number.set()
    else:
        if check_admin(message.from_user.id):
            await message.answer(messages.messages[f'admin_login_{BotDB.get_lang(message.from_user.id)}'],
                                 reply_markup=rk[f'main_admin_{BotDB.get_lang(message.from_user.id)}'])
        else:
            await message.answer(messages.messages[f'greeting_{BotDB.get_lang(message.from_user.id)}'],
                                 reply_markup=rk[f'main_{BotDB.get_lang(message.from_user.id)}'])


@dp.message_handler(state=User.user_number)
async def input_user_number(message: types.Message, state: FSMContext):
    number = message.text
    true_number = ''
    for i in number:
        if i in '0123456789':
            true_number += i
    BotDB.add_user(message.from_user.id, true_number)
    await message.answer(messages.messages[f'phone_num_access_{BotDB.get_lang(message.from_user.id)}'])
    await state.finish()
    if check_admin(message.from_user.id):
        await message.answer(messages.messages[f'greeting_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_admin_{BotDB.get_lang(message.from_user.id)}'])
    else:
        await message.answer(messages.messages[f'greeting_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_{BotDB.get_lang(message.from_user.id)}'])


@dp.message_handler(text=['Сменить номер телефона', 'Change phone number'])
async def change_phone_number(message: types.Message):
    await message.answer(messages.messages[f'input_new_phone_number_{BotDB.get_lang(message.from_user.id)}'])
    await User.new_user_number.set()


@dp.message_handler(state=User.new_user_number)
async def input_new_phone_number(message: types.Message, state: FSMContext):
    new_number = message.text
    true_number = ''
    for i in new_number:
        if i in '0123456789':
            true_number += i
    BotDB.change_phone_num(message.from_user.id, true_number)
    await state.finish()
    if check_admin(message.from_user.id):
        await message.answer(messages.messages[f'change_number_access_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_admin_{BotDB.get_lang(message.from_user.id)}'])
    else:
        await message.answer(messages.messages[f'change_number_access_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_{BotDB.get_lang(message.from_user.id)}'])


@dp.message_handler(text=['Информация', 'Info'])
async def info(message: types.Message):
    await message.bot.send_message(message.from_user.id,
                                   text=f'{messages.messages[f"info_{BotDB.get_lang(message.from_user.id)}"]}\n'
                                        f'Telegram id: {message.from_user.id}\n'
                                        f'{messages.messages[f"phone_num_{BotDB.get_lang(message.from_user.id)}"]} '
                                        f'{BotDB.get_user_phone(message.from_user.id)}')


@dp.message_handler(text=['Количество баллов', 'Points'])
async def points(message: types.Message):
    await message.bot.send_message(message.from_user.id,
                                   text=f'{messages.messages[f"points_{BotDB.get_lang(message.from_user.id)}"]} '
                                        f'{BotDB.get_points(message.from_user.id)}')


@dp.message_handler(text=['Админ-панель', 'Admin-panel'])
async def points(message: types.Message):
    if check_admin(message.from_user.id):
        await message.answer(messages.messages[f'admin_panel_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'admin_panel_{BotDB.get_lang(message.from_user.id)}'])
    else:
        await message.answer(messages.messages[f'message_error_{BotDB.get_lang(message.from_user.id)}'])


@dp.message_handler(text=['Создать рассылку', 'Create mailing list'])
async def create_mailing_list(message: types.Message):
    if check_admin(message.from_user.id):
        await message.answer(messages.messages[f'create_sendall_{BotDB.get_lang(message.from_user.id)}'])
    else:
        await message.answer(messages.messages[f'message_error_{BotDB.get_lang(message.from_user.id)}'])


@dp.message_handler(commands='sendall')
async def sendall(message: types.Message):
    if check_admin(message.from_user.id):
        if len(message.text) <= 9:
            await message.answer(messages.messages[f'error_sendall_{BotDB.get_lang(message.from_user.id)}'])
        else:
            text = message.text[9:]
            users = BotDB.get_users()
            for row in users:
                try:
                    await message.answer(row[0], text)
                except ValueError:
                    await message.answer(messages.messages[f'error_{BotDB.get_lang(message.from_user.id)}'])
            await message.answer(messages.messages[f'sendall_success_{BotDB.get_lang(message.from_user.id)}'])
    else:
        await message.answer(messages.messages[f'message_error_{BotDB.get_lang(message.from_user.id)}'])


@dp.message_handler(commands="getchatid")
async def cmd_test1(message: types.Message):
    await message.bot.send_message(message.from_user.id, message.chat.id)


@dp.message_handler(text=['Поддержка', 'Support'])
async def forward_message(message: types.Message):
    await message.answer(messages.messages[f'describe_error_{BotDB.get_lang(message.from_user.id)}'],
                         reply_markup=rk[f'extra_{BotDB.get_lang(message.from_user.id)}'])
    await User.text_of_the_appeal.set()


@dp.message_handler(state=User.text_of_the_appeal)
async def send_forward_message(message: types.Message, state: FSMContext):
    await message.bot.send_message(-995941442, '📫 | Новое обращение')
    await message.bot.forward_message(-995941442, message.from_user.id, message.message_id)
    await message.bot.send_message(-995941442,
                                   f'/responsetouser {message.from_user.id}')
    await state.finish()
    if check_admin(message.from_user.id):
        await message.answer(messages.messages[f'message_was_sended_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_admin_{BotDB.get_lang(message.from_user.id)}'])
    else:
        await message.answer(messages.messages[f'message_was_sended_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_{BotDB.get_lang(message.from_user.id)}'])


@dp.message_handler(commands='responsetouser')
async def response_to_user(message: types.Message):
    temp = message.text.split()
    text = ' '.join(temp[2:])
    await message.bot.send_message(temp[1], '📫 | Новое уведомление!\n'
                                            'Ответ от техподдержки:\n'
                                            '\n'
                                            f'<code>{text}</code>')


@dp.message_handler(text=['Отмена', 'Cancel'])
async def cancel(message: types.Message):
    if check_admin(message.from_user.id):
        await message.answer(messages.messages[f'choose_action_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_admin_{BotDB.get_lang(message.from_user.id)}'])
    else:
        await message.answer(messages.messages[f'choose_action_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_{BotDB.get_lang(message.from_user.id)}'])


@dp.message_handler(text=['Сменить язык', 'Change language'])
async def change_language(message: types.Message):
    await message.answer(messages.messages[f'choose_lang_{BotDB.get_lang(message.from_user.id)}'],
                         reply_markup=languages)


@dp.callback_query_handler(lambda c: c.data == 'buttonRus')
async def process_callback_buttonRus(call: types.CallbackQuery):
    await call.bot.answer_callback_query(call.id, 'Выбран русский язык')
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.bot.send_message(call.from_user.id, 'Введите команду /start')
    BotDB.change_lang(call.from_user.id, 'Rus')


@dp.callback_query_handler(lambda c: c.data == 'buttonEng')
async def process_callback_buttonEng(call: types.CallbackQuery):
    await call.bot.answer_callback_query(call.id, 'English changed')
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.bot.send_message(call.from_user.id, 'Enter command /start')
    BotDB.change_lang(call.from_user.id, 'Eng')


async def show_keyboard(message: types.Message):
    await message.answer(text='клавиатура', reply_markup=rk[f'main_Rus'])


@dp.message_handler()
async def pass_func(message: types.Message):
    if check_admin(message.from_user.id):
        await message.answer(messages.messages[f'message_error_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_admin_{BotDB.get_lang(message.from_user.id)}'])
    else:
        await message.answer(messages.messages[f'message_error_{BotDB.get_lang(message.from_user.id)}'],
                             reply_markup=rk[f'main_{BotDB.get_lang(message.from_user.id)}'])
