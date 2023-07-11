from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import messages
from dispatcher import dp
from main import BotDB
from keyboards.default.Keyboards import ReplyKeyboadrs as rk
from keyboards.inline.Inline import *
import hashlib
from functions.Functions import check_admin

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or "echo"
    link = text
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id = result_id,
        title='текст',
        url=link,
        input_message_content=types.InputTextMessageContent(
            message_text=link
        )
    )]

    await query.answer(articles, cache_time=1, is_personal=True)
