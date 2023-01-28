import asyncio
import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound
from contextlib import suppress
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from config import TOKEN, PAYMENT_TOKEN
from messages import MESSAGES
import keyboards as kb
from keyboards import Keyboard

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token = TOKEN, parse_mode = types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop = loop)


async def delete_message(message, sleep_time = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(commands = ['testdel'])
async def process_del_message(message):
    msg = await bot.send_message(message.from_user.id, 'Я удалюсь через 3 секунды')
    asyncio.create_task(delete_message(msg, 3))


@dp.message_handler(commands = ['start'])
async def process_start_command(message):
    await message.reply(MESSAGES['start'].format(user_name = message.from_user.first_name, user_last_name = message.from_user.last_name), reply = False)

@dp.message_handler(commands = ['help'])
async def process_help_command(message):
    await message.reply(MESSAGES['help'], reply = False)


@dp.message_handler(commands = ['cat'])
async def process_cat_command(message):
    await message.reply('Категории:', reply = False, reply_markup = kb.category_kb)
    

@dp.message_handler(commands = ['rm'])
async def process_remove_keyboard(message):
    await message.reply('Убрал шаблоны', reply = False, reply_markup = kb.ReplyKeyboardRemove())

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_categories(callback_query):
    category = callback_query.data[3:]
    # await bot.answer_callback_query(callback_query.id, text = category.title())
    # await bot.send_message(callback_query.from_user.id, f'Категория {category.title()}:', reply_markup = kb.get_keyboard(kb.keyboards[category]))
    # await callback_query.edit_message(reply_markup = kb.get_keyboard(kb.keyboards[category]))
    await callback_query.message.edit_reply_markup(kb.keyboards[category].keyboards[0])

@dp.callback_query_handler(lambda c: c.data and (c.data.startswith('next') or c.data.startswith('previous')))
async def process_callback_next_page(callback_query):
    if callback_query.data.startswith('next'):
        category = callback_query.data[4:-1]
    else:
        category = callback_query.data[8:-1]
    page = int(callback_query.data[-1])
    await callback_query.message.edit_reply_markup(kb.keyboards[category].keyboards[page])


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cat'))
async def process_callback_goods(callback_query):
    category = callback_query.data[3:]
    # print(kb.Keyboard.cats_to_urls[category])
    # keyboard = kb.InlineKeyboardMarkup()
    # keyboard.add(kb.InlineKeyboardButton(Keyboard.cats_to_urls[category], callback_data=category))
    await callback_query.message.edit_text(text = category, reply_markup = kb.KeyboardGoods(category).keyboards[0])



@dp.callback_query_handler(lambda c: c.data == 'home')
async def process_callback_home(callback_query):
    await callback_query.message.edit_reply_markup(kb.category_kb)
    

# @dp.message_handler(commands = ['test'])
# async def process_test(message):
#     print(kb.cats_to_urls)


@dp.message_handler()
async def process_echo_message(message):
    await message.reply(message.text)



if __name__ == '__main__':
    executor.start_polling(dp, loop = loop)
