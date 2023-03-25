from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


# @dp.message_handler(CommandHelp())
# async def bot_help(message: types.Message):
#     text = ("Buyruqlar: ",
#             "/start - Botni qaytadan ishga tushurish",
#             "/help - Yordam")
#
#     await message.answer("\n".join(text))


@dp.message_handler(CommandHelp())
async def helps(message: types.Message):
    txt = 'Admin bilan bog\'lanish @status_developer'
    await message.answer(txt)
