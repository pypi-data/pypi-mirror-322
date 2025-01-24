from getpass import getpass
from typing import Optional

import aiosqlite
from fastapi import Depends
from pydantic import BaseModel, constr

from .constants import oauth2_scheme
from .exceptions import (
    DatabaseError,
    FastAuthException,
    InvalidPassword,
    CredentialsException,
    UserNotFound,
)
from .funcs import replace, get_data_from_token, insert
from .funcs import get_password_hash as _hash
from .funcs import verify_password as _verify
from .settings import settings


class User(BaseModel):
    __table__ = "users"
    username: str
    password: str

    def check_password(self, password):
        return _verify(password, self.password)

    @staticmethod
    def hash_password(password):
        return _hash(password)

    @classmethod
    def create_table_query(cls):
        return f"""
        CREATE TABLE IF NOT EXISTS {cls.__table__} (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
        """

    @classmethod
    async def create_table(cls):
        # Check if the table already exists
        async with aiosqlite.connect(settings.user_db_path) as db:
            async with db.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                (cls.__table__,),
            ) as cursor:
                if await cursor.fetchone():
                    return

        async with aiosqlite.connect(settings.user_db_path) as db:
            await db.execute(cls.create_table_query())
            await db.commit()

    @classmethod
    async def get(cls, username):
        async with aiosqlite.connect(settings.user_db_path) as db:
            async with db.execute(
                f"SELECT * FROM users WHERE username = ?;", (username,)
            ) as cursor:
                from_db = await cursor.fetchone()
                if from_db is None:
                    return None
                return cls(username=from_db[0], password=from_db[1])

    async def save(self):
        if len(self.password) != 60:
            self.password = self.hash_password(self.password)
        await replace(
            self.__table__, {"username": self.username, "password": self.password}
        )

    @staticmethod
    def sanitise_username(username: str):
        """
        Sanitise the username by taking only the first word and converting to lowercase

        :param username: str - the username to sanitise
        :return: str - the sanitised username
        """
        return username.split(" ")[0].lower()

    @classmethod
    async def create(cls, username: str, password: constr(max_length=59)):
        password = cls.hash_password(password)
        username = cls.sanitise_username(username)
        try:
            await insert(cls.__table__, {"username": username, "password": password})
        except aiosqlite.IntegrityError as e:
            raise DatabaseError(f"Could not create user `{username}`; {e}")

        return cls(username=username, password=password)

    async def update_password(self, old_password, password: constr(max_length=59)):
        if not self.check_password(old_password):
            raise InvalidPassword
        self.password = self.hash_password(password)
        await self.save()

    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Optional["User"]:
        user = await cls.get(username=username)
        if user is None:
            raise UserNotFound
        try:
            if not _verify(password, user.password):
                raise InvalidPassword
            return user
        except Exception:
            raise CredentialsException


async def logged_in_user(token: str = Depends(oauth2_scheme)):
    data = await get_data_from_token(token)
    user = await User.get(username=data.username)
    if user is None:
        raise UserNotFound
    return user


if __name__ == "__main__":
    import asyncio

    async def run():
        print(f"Creating `{User.__table__}` table")
        await User.create_table()
        print("Table created!")

        suggestion = "[Y/n]"
        check = {"y", "yes", ""}
        article = "a"

        while input(f"Create {article} user? {suggestion}: ").strip().lower() in check:
            username = input("Username: ")
            password = getpass("Password: ")
            password_confirm = getpass("Confirm password: ")
            if password != password_confirm:
                print("Passwords do not match!")
                continue
            try:
                await User.create(username, password)
            except FastAuthException as e:
                print(f"Error creating user: {e}")
                continue
            print(f"User `{username}` created!")

            suggestion = "[y/N]"
            check = {"n", "no", ""}
            article = "another"

    try:
        asyncio.run(run())
        print("Done!")
    except KeyboardInterrupt:
        print("\nExiting...")
