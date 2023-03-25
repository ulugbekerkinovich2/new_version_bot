import asyncio
import datetime

import psycopg2

from loader import bot


async def my_func():
    now = datetime.datetime.now()
    # if now.weekday() == 6 and now.hour == 20 and now.minute == 51:
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='order_bot',
        user='postgres',
        password='0852'
    )
    cur = conn.cursor()

    cur.execute('select full_name, telegram_id, url from children')
    rows = cur.fetchall()
    for row in rows:
        name = row[0]
        chat_id = row[1]
        link = row[2]
        print(name)
        print(chat_id)
        print(link)
        await bot.send_message(chat_id=chat_id, text=f'{name} uchun link {link}')
    # await bot.send_message(chat_id=935920479, text=)


async def main():
    while True:
        print(1)
        await my_func()
        await asyncio.sleep(60)  # sleep for 1 minute


if __name__ == '__main__':
    asyncio.run(main())