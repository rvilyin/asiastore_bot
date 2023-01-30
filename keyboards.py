
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database.views import *
from database.settings import db
from parse import *


db.connect()
Goods.create_table()
delete_all()

def btn(name):
    name2 = ''.join([x for x in name if x.isalpha()])
    return InlineKeyboardButton(name, callback_data = 'btn' + name2.lower())


# def get_keyboard(url):
#     categories = get_categories(BASE_URL + url)
#     category_kb = InlineKeyboardMarkup(row_width = 1)
#     for cat in categories:
#         category_kb.insert(btn(cat))

#     return category_kb


class Keyboard:
    cats_to_urls = {}
    def __init__(self, url, name):
        categories_urls = get_categories(url)
        categories = list(categories_urls.keys())
        categories2 = self.divide_cats(categories)
        Keyboard.cats_to_urls.update(categories_urls)
        self.keyboards = self.get_keyboards(categories2, name)
        self.name = name
        self.url = url
    
    @staticmethod
    def divide_cats(categories):
        # print(categories)
        new_categories = []
        a = []
        for i in range(len(categories)):
            a.append(categories[i])
            if (i+1) % 5 == 0 or i == len(categories)-1:
                new_categories.append(a)
                a = []

        return new_categories

    @staticmethod
    def add_categories_to_keyboard(categories):
        kb = InlineKeyboardMarkup(row_width = 1)
        for category in categories:
            kb.insert(InlineKeyboardButton(category, callback_data = 'cat' + category))
        return kb

    @staticmethod
    def previous_button(name, i):
        return InlineKeyboardButton('<<', callback_data='previous' + name + ',' + str(i-1))

    @staticmethod
    def next_button(name, i):
        return InlineKeyboardButton('>>', callback_data='next' + name + ',' + str(i+1))

    def get_keyboards(self, categories, name):
        kbs = []
        if len(categories) == 1:
            kbs.append(self.add_categories_to_keyboard(categories[0]).add(
                InlineKeyboardButton('🏠', callback_data = 'home')
            ))
            return kbs
        for i in range(len(categories)):
            kb = self.add_categories_to_keyboard(categories[i])
            if i == 0:
                kb.add(self.next_button(name, i))
            elif i == len(categories) - 1:
                kb.add(self.previous_button(name, i))
            else:
                kb.row(self.previous_button(name, i), self.next_button(name, i))
            kb.add(InlineKeyboardButton('🏠', callback_data = 'home'))
            kbs.append(kb)
        
        return kbs


class KeyboardGoods(Keyboard):
    goods_to_keyboards = {}
    def __init__(self, category):
        if category not in KeyboardGoods.goods_to_keyboards.keys():
            goods_urls = parse_goods(Keyboard.cats_to_urls[category])
            for good, url in goods_urls.items():
                post_good(good, url)
            goods2 = self.divide_cats(list(goods_urls.keys()))
            keyboards = self.get_keyboards(goods2, category)
            KeyboardGoods.goods_to_keyboards.update({category: keyboards})



    def add_categories_to_keyboard(self, goods):
        kb = InlineKeyboardMarkup(row_width = 1)
        for j in range(len(goods)):
            good = goods[j]
            if good.startswith('iPhone'):
                index = good.find(',') + 1
                name = good[index:]
            elif good.startswith('Apple Mac Studio'):
                name = self.get_macstudio_name(good)
            kb.insert(InlineKeyboardButton(name, callback_data = 'good' + str(get_id_by_name(good))))
        return kb

    @staticmethod
    def get_macstudio_name(name):
        l = name.split(',')
        index = l[1].index('(')
        l[1] = l[1][1:index-1]
        return ','.join(l[1:-1])
        


category_kb = InlineKeyboardMarkup(row_width = 1).add(
    btn('iPhone📱'),
    btn('Mac💻'),
    btn('iPad✏️📲'),
    btn('Watch⌚️'),
    # btn('AirPods'),
    btn('Garmin⌚️'),
    btn('Accessories🖱'),
    btn('JBL🎧'),
    btn('Beats🎧'),
    btn('Gadgets🎮'),
    btn('Yandex📻')
)


keyboards = {
    'iphone': Keyboard('apple-iphone/', 'iphone'),
    'mac': Keyboard('apple-mac/', 'mac'),
    'ipad': Keyboard('apple-ipad/', 'ipad'),
    'watch': Keyboard('apple-watch/', 'watch'),
    # 'airpods': Keyboard('apple-airpods/', 'airpods'),
    'garmin': Keyboard('garmin/', 'garmin'),
    'accessories': Keyboard('accessories/', 'accessories'),
    'jbl': Keyboard('jbl/', 'jbl'),
    'beats': Keyboard('beats/', 'beats'),
    'gadgets': Keyboard('gadgets/', 'gadgets'),
    'yandex': Keyboard('yandex-station/', 'yandex')
}

with open('categories.txt', 'wt') as file:
    for url in Keyboard.cats_to_urls.values():
        file.write(url + '\n')



def main():
    k1 = Keyboard('apple-iphone/', 'iphone')
    print(k1.categories)


if __name__ == '__main__':
    main()


