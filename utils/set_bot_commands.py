from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start"),
            # types.BotCommand("set link", "link biriktirish"),
            # types.BotCommand('register', 'ro\'yhatdan o\'tish')
        ]
    )
