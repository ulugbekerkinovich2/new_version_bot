import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    # for admin in ADMINS:
    #     print(admin, type(admin))
    #     try:
    #         await dp.bot.send_message(admin, "Bot ishga tushdi")
    #
    #     except Exception as err:
    #         logging.exception(err)
    await dp.bot.send_message(ADMINS[0], 'Bot ishga tushdi')
