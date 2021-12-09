from tortoise.models import Model
from tortoise import fields, Tortoise

class Users(Model):
    id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField(unique=True)


class Books(Model):
    id = fields.BigIntField(pk=True)
    book_url = fields.TextField(max_length=255)
    hash_id = fields.TextField(max_length=255)
    title = fields.TextField(max_length=2550)
    file_id = fields.TextField(max_length=2550, null=True)
    

async def connect_database():
    await Tortoise.init(
        db_url="sqlite://database.db", modules={"models": [__name__]}
    )
    await Tortoise.generate_schemas()