import peewee
from database.models import Goods



def post_good(good_name, good_url):
    try:
        good = Goods(name = good_name, url = good_url)
        good.save()
    except peewee.IntegrityError:
        print('Такой товар уже существует!')

def get_id_by_name(name_good):
    try:
        good = Goods.get(name = name_good)
        return good.id
    except peewee.DoesNotExist:
        print('Нет такой категории')
    
def get_good(id_good):
    try:
        good = Goods.get(id = id_good)
        return good.name, good.url
    except peewee.DoesNotExist:
        print('Нет такой категории')

def delete_good(name_good):
    try:
        good = Goods.get(name = name_good)
        good.delete_instance()
    except peewee.DoesNotExist:
        print('Категория не найдена!')

def delete_all():
    goods = Goods.select()
    for good in goods:
        good.delete_instance()

def get_goods():
    goods = Goods.select()
    goods_info = {good.id: (good.name, good.url) for good in goods}
    return goods_info
