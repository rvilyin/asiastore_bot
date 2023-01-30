import peewee
from database.settings import db


class Goods(peewee.Model):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(max_length = 100, unique = True)
    url = peewee.CharField(max_length = 150, unique = True)

    class Meta:
        database = db
        db_table = 'goods_urls'

