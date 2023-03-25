import random
import re

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from filters.private_chat import IsPrivate
from keyboards.default.startKeyboard import children
from keyboards.inline.register_inline import register_inline
from loader import dp, db, bot
from states.register import Register, Children_Register


@dp.message_handler(text='/delete_users')
async def delete_user(message: types.Message):
    if f'{message.chat.id}' in ADMINS:
        await db.delete_users()
        await message.answer('Barcha foydalanuvchilar o\'chirildi')
    else:
        await message.answer('Sizga ushbu buyruqqa murojat qilish ruxsat etilmagan')


@dp.message_handler(text='/delete_register')
async def delete_register(message: types.Message):
    if f'{message.chat.id}' in ADMINS:
        await db.delete_registers()
        await db.delete_children()
        await message.answer("Barcha start bosganlar o\'chirildi")
    else:
        await message.answer('Sizga ushbu buyruqqa murojat qilish ruxsat etilmagan')


@dp.message_handler(text='/statistika')
async def count(message: types.Message):
    if f'{message.from_user.id}' in ADMINS:
        counts = await db.count_users()
        registers = await db.count_registers()
        await message.answer(
            f'<b>Bot foydalanuvchilari soni:</b> {registers}\n<b>Botga start bosganlar soni:</b>{counts}',
            parse_mode='HTML')


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    # print(ADMINS, type(ADMINS), type(ADMINS[0]), message.chat.id)
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)
    await message.answer(f"<b>Hayrli kun {message.from_user.full_name} , kuningiz barakali o'tsin</b>",
                         parse_mode='HTML')
    chat_id = -1001627440366
    await message.answer(text=f'Bu yerda bot haqida ma\'lumot bo\'ladi')
    await message.answer("<b>To'liq ismingizni kiriting:</b>\nMisol uchun: Alisher Usmonov", parse_mode='HTML',
                         reply_markup=ReplyKeyboardRemove())
    # if message.text != '/start':
    await Register.name.set()


@dp.message_handler(state=Register.name)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data(name=fullname)
    await message.answer('<b>☎️ Telefon raqamingizni kiriting</b>\nMisol uchun: +998912543636', parse_mode='HTML')
    await Register.number.set()


@dp.message_handler(state=Register.number)
async def answer_phone_number(message: types.Message, state: FSMContext):
    phone = message.text
    # if phone.isalnum() or len(phone) < 9:
    #     await message.reply('Raqamingizni kiriting...')
    await state.update_data(number=phone)

    data = await state.get_data()
    name1 = data.get("name")
    number1 = data.get("number")
    try:
        await db.add_register(telegram_id=message.from_user.id,
                              full_name=name1,
                              phone_number=number1,
                              username=message.from_user.username)
    except Exception as e:
        await message.answer('Siz ro\'yhatdan o\'tgansiz!!!✅', reply_markup=children)
        await state.finish()
    # await db.select_anketa(telegram_id=message.from_user.id)
    # msg = "Quyidagi ma'lumotlar qabul qilindi:\n"
    # msg += f"Ismingiz - {name1}\n"
    # msg += f"Telefon raqam - {number1}"
    # await message.answer(msg)
    await message.answer("Ma'lumotlar muvaffaqiyatli saqlandi!✅", reply_markup=children)

    count1 = await db.count_users()

    msg = f"{message.from_user.full_name} @{message.from_user.username}" \
          f" ro\'yhatdan o\'tdi.\nBazada {count1} ta foydalanuvchi bor."
    await bot.send_message(chat_id=-1001867869015, text=msg)
    await state.finish()


@dp.message_handler(IsPrivate(), text='Farzand ma\'lumotlarini ro\'yhatdan o\'tkazish')
async def register_children(message: types.Message):
    await message.answer("<b>Farzandingiz ismini kiriting:</b>\nMisol uchun: Shahzoda Karimova", parse_mode='HTML')
    await Children_Register.name.set()


@dp.message_handler(state=Children_Register.name)
async def answer_children_name(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data(child_name=fullname)
    await message.answer('<b>☎️ Farzandingizni telefon raqamini kiriting</b>\nMisol uchun: +998978365656',
                         parse_mode='HTML')
    await Children_Register.number.set()


@dp.message_handler(state=Children_Register.number)
async def answer_children_number(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data(children_number=number)
    data = await state.get_data()
    children_name = data.get('child_name')
    children_phone = data.get('children_number')
    full_name = await db.select_parent_name(
        telegram_id=message.from_user.id
    )
    parent_phone = await db.select_parent_phone(
        telegram_id=message.from_user.id
    )
    try:
        code = ''.join(str(random.randint(0, 9)) for _ in range(10))
        await db.add_children(
            telegram_id=message.from_user.id,
            full_name=children_name,
            phone_number=children_phone,
            parent_name=full_name,
            username=message.from_user.username,
            code=code
        )
        await message.answer("Farzandingiz ma'lumotlari muvaffaqiyatli qo'shildi ✅")
        # await message.answer(
        #     "Yana Farzandingiz ma\'lumotlarini qo\'shish uchun \nFarzand ma\'lumotlarini ro\'yhatdan o\'tkazish tugmasini bosing ")
        mess = f'<b>id:</b> {code}\n' \
               f'<b>Ota-ona:</b> {full_name}\n' \
               f'<b>Ota-ona telefon raqami:</b> {parent_phone}\n' \
               f'<b>Farzandini ismi:</b> {children_name}\n' \
               f'<b>Farzandini telefon raqami:</b> {children_phone}'
        chat_id1 = -1001627440366
        chat_id2 = -1001867869015
        await bot.send_message(chat_id=chat_id1, text=mess, reply_markup=register_inline)  # real group
        await bot.send_message(chat_id=chat_id2, text=mess, parse_mode='HTML', reply_markup=register_inline)

        chat_id = -1001627440366
        await bot.send_message(chat_id=chat_id, text=mess, reply_markup=register_inline)

    except Exception as e:
        await message.answer("Farzandingiz ma\'lumotlari qo\'shilmadi ⚠️\nQaytadan urinib ko\'ring",
                             reply_markup=children)
        await bot.send_message(chat_id=-1001867869015, text=e)
        await state.finish()

    counts = await db.count_children()
    msg = f"Ota-ona {message.from_user.full_name} @{message.from_user.username}" \
          f" farzandi ma'lumotlari qo'shildi.\nBazada ota-onani {counts} ta farzandi bor."
    await bot.send_message(chat_id=-1001867869015, text=msg)
    await state.finish()


@dp.message_handler(text='Yakunlash')
async def yakunlash(message: types.Message):
    await message.answer(text='Ro\'yhatdan o\'tkazish yakunlandi✅', reply_markup=ReplyKeyboardRemove())
