from peewee import SqliteDatabase, Model, CharField, BooleanField, DateField, ForeignKeyField


db = SqliteDatabase('bot.sqlite3')


class User(Model):
    chat_id = CharField()

    class Meta:
        database = db


class Todo(Model):
    task = CharField()
    is_done = BooleanField()
    date = DateField()
    user = ForeignKeyField(User)

