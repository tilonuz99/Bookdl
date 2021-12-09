from os import system

from hashlib import md5

from pyrogram import Client, idle

from tortoise import Tortoise, run_async

from database.model import connect_database


APP_ID = 448835
API_HASH = "13c1afbfbcf7dd8480c4c58a08bf0011"
API_TOKEN = "1375519356:AAHutkxbBk6oe5Cl7IoDIye8Fm5ddZevfc4"


client = Client(
    "booksearch",
    bot_token=API_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins")
)


async def startup():
    await client.start()
    await connect_database()
    await idle()
    system('clear')


if __name__ == "__main__":
    try:
        run_async(startup())
    except KeyboardInterrupt:
        Tortoise.close_connections()
