import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from filters.group_filter import IsGroup
from loader import dp, db, bot


# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     await message.answer(f"Hayrli kun {message.from_user.full_name} , kuningiz barakali o'tsin")


@dp.message_handler(IsGroup(), CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    await message.answer(f"<b>Hayrli kech {message.from_user.full_name} , kuningiz barakali o'tsin</b>",
                         parse_mode='HTML',
                         reply_markup=ReplyKeyboardRemove())

    # ADMINGA xabar beramiz
    count = await db.count_users()
    msg = f"{user[1]} @{message.from_user.username} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    # await bot.send_message(chat_id=ADMINS[0], text=msg, reply_markup=menu)
    await bot.send_message(chat_id=-1001867869015, text=msg)
