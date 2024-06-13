from telebot import types


def admin_start_btn():

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    btn_1 = types.InlineKeyboardButton(text='Добавить нового плательщика', callback_data='add_new')
    btn_2 = types.InlineKeyboardButton(text='Изменить плательщика', callback_data='change')
    btn_3 = types.InlineKeyboardButton(text='Продлить плательщика', callback_data='renew')
    btn_4 = types.InlineKeyboardButton(text='Удалить плательщика', callback_data='cancel')
    btn_5 = types.InlineKeyboardButton(text='Проверить плательщика', callback_data='check')
    btn_6 = types.InlineKeyboardButton(text='Статистика', callback_data='stat')

    keyboard.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6)

    return keyboard
