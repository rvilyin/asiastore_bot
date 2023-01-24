
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from parse import *


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
    def __init__(self, url, name):
        categories = get_categories(BASE_URL + url)
        categories2 = self.divide_cats(categories)
        self.keyboards = self.get_keyboards(categories2, name)
        self.name = name
        self.url = url
    
    @staticmethod
    def divide_cats(categories):
        print(categories)
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
        for j in categories:
            kb.insert(InlineKeyboardButton(j, callback_data = 'cat' + j.lower()))
        return kb

    @staticmethod
    def get_keyboards(categories, name):
        kbs = []
        if len(categories) == 1:
            kbs.append(Keyboard.add_categories_to_keyboard(categories[0]).add(
                InlineKeyboardButton('🏠', callback_data = 'home')
            ))
            return kbs
        for i in range(len(categories)):
            kb = Keyboard.add_categories_to_keyboard(categories[i])
            if i == 0:
                kb.add(InlineKeyboardButton('>>', callback_data = 'next' + name + str(i+1)))
            elif i == len(categories) - 1:
                kb.add(InlineKeyboardButton('<<', callback_data = 'previous' + name + str(i-1)))
            else:
                kb.row(
                    InlineKeyboardButton('<<', callback_data = 'previous' + name + str(i-1)),
                    InlineKeyboardButton('>>', callback_data = 'next' + name + str(i+1))
                )
            kb.add(InlineKeyboardButton('🏠', callback_data = 'home'))
            kbs.append(kb)
        

        return kbs

        
        


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


def main():
    k1 = Keyboard('apple-iphone/', 'iphone')
    print(k1.categories)


if __name__ == '__main__':
    main()


