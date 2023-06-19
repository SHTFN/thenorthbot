from aiogram.types import ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Информация').add('Количество баллов').add('Поддержка')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Информация').add('Количество баллов').add('Поддержка').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Создать рассылку').add('Назад')

extra = ReplyKeyboardMarkup(resize_keyboard=True)
extra.add('Отмена')
