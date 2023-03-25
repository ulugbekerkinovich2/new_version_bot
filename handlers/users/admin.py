import datetime
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message

from data import config
from data.config import ADMINS
from filters.group_filter import IsGroup
from keyboards.inline.register_inline import register_inline
from loader import dp, db, bot
from states.register import Children_Link, Set_Link
from utils.db_api.postgresql import Database


@dp.message_handler(text="/users")
async def get_users(message: types.Message):
    if f'{message.from_user.id}' in ADMINS:
        get_user = await db.select_all_users()
        # print(get_user)
        # get_children = await db.select_all_children()
        # print(get_children)
        try:
            k = len(get_user)
            for i in get_user:
                user_id = i[0]
                user_name = i[1]
                user_nick = i[2]

                # print(user_id, i)
                await bot.send_message(chat_id=ADMINS[0],
                                       text=f'<b>{user_id}</b>' '.' f"<b>  {user_name}</b>" f"  @{user_nick} ",
                                       parse_mode='HTML')
            await bot.send_message(chat_id=ADMINS[0], text=f"\n{k} ta user mavjud")
        except:
            await bot.send_message(chat_id=ADMINS[0], text="foydalanuvchilar o'chirilgan")


@dp.callback_query_handler(text='link')
async def set_link(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Linkni yuboring: ')
    await Set_Link.link.set()

    # Get the text of the message containing the inline keyboard
    message_text = call.message.text.split('\n')
    message_text = ' '.join(map(str, message_text))
    message_text_id = message_text.split(' ')[1]

    # Save message_text_id to state
    await state.update_data(message_text_id=message_text_id)

    # Print the text under the inline keyboard
    print(message_text_id)


@dp.message_handler(state=Set_Link.link)
async def get_link(message: Message, state: FSMContext):
    link = message.text

    # Get message_text_id from state
    data = await state.get_data()
    message_text_id = data.get('message_text_id')

    await db.update_children_link(link, message_text_id)
    print(f"User entered link: {link}\n {message}")
    await message.answer("Link biriktirildi✅")
    await state.finish()


# @dp.message_handler(state=Children_Link.telegram_id)
# async def get_id(message: types.Message, state: FSMContext):
#     code = message.text
#     await state.update_data(code=code)
#     await message.answer('Linkni yuboring: ')
#     await Children_Link.link.set()
#
#
# @dp.message_handler(state=Children_Link.link)
# async def get_link(message: types.Message, state: FSMContext):
#     link = message.text
#     print(link)
#     await state.update_data(student_link=link)
#     data = await state.get_data()
#     code = data.get('code')
#     link = data.get('student_link')
#     try:
#         await db.update_children_link(
#             code=code,
#             link=link
#         )
#         await message.answer('Link biriktirildi ✅')
#     except Exception as e:
#         await message.answer('Link biriktirilmadi qaytadan urinib ko\'ring')
#         await bot.send_message(chat_id=-1001867869015, text=link)
#         await state.finish()
#     await state.finish()


# async def send_message():
#     now = datetime.datetime.now()
#     current_year = now.year
#     current_month = now.month
#     current_day = now.day
#     weekday_name = datetime.date(current_year, current_month, current_day).strftime("%A")
#     print(weekday_name)
#     db = Database(dsn=config.DSN)  # create a new instance of the Database class
#     await db.create()  # create the connection pool
#
#     if weekday_name == "Tuesday":
#         data = await db.execute("SELECT user_id FROM users")  # execute the query using the connection pool
#         for row in data:
#             user_id = row[0]
#             message = "Hello, this is a message sent to all users on Tuesday at 08:00."
#             await bot.send_message(chat_id=user_id, text=message)
#
#     await db.close_pool()  # close the connection pool
