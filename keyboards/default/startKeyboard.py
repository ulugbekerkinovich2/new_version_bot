from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Telefon raqamni yuborish', request_contact=True)
        ],
    ],
    resize_keyboard=True
)

children = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Farzand ma\'lumotlarini ro\'yhatdan o\'tkazish'),
            KeyboardButton(text='Yakunlash')
        ],
    ],
    resize_keyboard=True
)
set_link = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Linkni biriktirish')
        ],
    ],
    resize_keyboard=True
)