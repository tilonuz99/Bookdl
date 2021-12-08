from Bookdl.pdfdrive import search

from aiogram import Dispatcher, Bot, executor, types


API_TOKEN = "1375519356:AAHutkxbBk6oe5Cl7IoDIye8Fm5ddZevfc4"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Kitoblar olami)")

@dp.message_handler(content_types='text', chat_type='private')
async def search_book(message: types.Message):
    results = await search(message.text)
    searched_results = "Natijalar: \n\n"
    i = 0
    for x, result in enumerate(results.values()):
        title, url = result
        i += 1
        searched_results += f"{i}. <b>{title}</b>\n"
    await message.reply(searched_results, parse_mode='html')

executor.start_polling(dp)
