from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_Rus = ReplyKeyboardMarkup(resize_keyboard=True)
# main_Rus.add('Информация').add('Количество баллов').add('Поддержка').add('Сменить язык')
main_Rus.row(KeyboardButton('Информация'),
             KeyboardButton('Поддержка')) \
    .row(KeyboardButton('Сменить язык'),
         KeyboardButton('Сменить номер телефона'))

main_admin_Rus = ReplyKeyboardMarkup(resize_keyboard=True)
# main_admin_Rus.add('Информация').add('Количество баллов').add('Поддержка').add('Сменить язык').add('Админ-панель')
main_admin_Rus.row(KeyboardButton('Информация'),
                   KeyboardButton('Поддержка'),
                   KeyboardButton('Каталог')) \
    .row(KeyboardButton('Сменить язык'),
         KeyboardButton('Сменить номер телефона')) \
    .add('Админ-панель')

admin_panel_Rus = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel_Rus.add('Создать рассылку') \
    .row(KeyboardButton('Добавить товар'),
         KeyboardButton('Удалить товар')) \
    .add('Назад')

catalog_panel_Rus = ReplyKeyboardMarkup(resize_keyboard=True)
catalog_panel_Rus.row(KeyboardButton('Выбрать товар'),
                      KeyboardButton('Назад'))

extra_Rus = ReplyKeyboardMarkup(resize_keyboard=True)
extra_Rus.add('Отмена')

main_Eng = ReplyKeyboardMarkup(resize_keyboard=True)
main_Eng.row(KeyboardButton('Info'), KeyboardButton('Points')).row(KeyboardButton('Support'),
                                                                   KeyboardButton('Change language'))

main_admin_Eng = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin_Eng.row(KeyboardButton('Info'), KeyboardButton('Points')).row(KeyboardButton('Support'),
                                                                         KeyboardButton('Change language')).add(
    'Admin-panel')

admin_panel_Eng = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel_Eng.add('Create mailing list').add('Back')

extra_Eng = ReplyKeyboardMarkup(resize_keyboard=True)
extra_Eng.add('Cancel')

ReplyKeyboadrs = {
    'main_Rus': main_Rus,
    'main_admin_Rus': main_admin_Rus,
    'admin_panel_Rus': admin_panel_Rus,
    'extra_Rus': extra_Rus,
    'main_Eng': main_Eng,
    'main_admin_Eng': main_admin_Eng,
    'admin_panel_Eng': admin_panel_Eng,
    'extra_Eng': extra_Eng,
    'catalog_panel_Rus': catalog_panel_Rus
}
