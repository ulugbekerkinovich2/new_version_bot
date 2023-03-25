from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

register_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🔗 link biriktirish', callback_data='link')
        ]
    ]
)
