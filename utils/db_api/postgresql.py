from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=config.DB_PORT
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_table_register(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Register (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        username VARCHAR(255) NOT NULL 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_table_children(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Children (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL,
        parent_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        url VARCHAR(4096) DEFAULT 'none',
        code VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # 'https://airtable.com/shrD4By42z2db21If/tblf7h4kwYw8bilLn'
    # async def get_parent(self, telegram_id):
    #     sql = "SELECT * FROM Register WHERE telegram_id=$1"
    #     return await self.execute(sql, telegram_id, fetchrow=True)

    async def add_children(self, telegram_id, full_name, phone_number, parent_name, username, code):
        sql = "INSERT INTO Children (telegram_id,full_name,phone_number, parent_name, username, code) VALUES($1,$2,$3,$4,$5,$6) returning *"
        return await self.execute(sql, telegram_id, full_name, phone_number, parent_name, username, code, fetchrow=True)

    async def add_register(self, full_name, phone_number, telegram_id, username):
        sql = "INSERT INTO register (full_name, phone_number, telegram_id, username) VALUES($1, $2, $3,$4) returning *"
        return await self.execute(sql, full_name, phone_number, telegram_id, username, fetchrow=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_parent_name(self, telegram_id):
        sql = 'SELECT full_name from register WHERE telegram_id=$1'
        return await self.execute(sql, telegram_id, fetchval=True)

    async def select_parent_phone(self, telegram_id):
        sql = 'SELECT phone_number FROM register WHERE telegram_id=$1'
        return await self.execute(sql, telegram_id, fetchval=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_children(self, **kwargs):
        sql = "SELECT * FROM Children"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def count_registers(self):
        sql = "SELECT COUNT(*) FROM Register"
        return await self.execute(sql, fetchval=True)

    async def count_children(self):
        sql = "SELECT COUNT(*) FROM Children"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_children_link(self, link, code):
        sql = 'UPDATE Children SET url=$1 WHERE code=$2'
        return await self.execute(sql, link, code, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_children(self):
        await self.execute('DELETE FROM Children WHERE TRUE', execute=True)

    async def delete_registers(self):
        await self.execute("DELETE FROM Register WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
