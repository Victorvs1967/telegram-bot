from config import API_TOKEN, DB_FILE
from dblighter import DbLighter
from parser import Parser

from aiogram import Bot, Dispatcher, executor, types
import logging
import asyncio


"""Configure logging"""
logging.basicConfig(level=logging.INFO)

"""Initialize bot and dispatcher"""
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = DbLighter()

# for SQLight
# db = DbLighter(DB_FILE) 

sg = Parser('lastkey.txt')


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exist(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id)
	
    await message.answer('You are success subscribed!')

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exist(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
    else:
        db.update_subscription(message.from_user.id, False)

    await message.answer('You are success unsubsribed!')

async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_games = sg.new_games()

		if(new_games):
			# если игры есть, переворачиваем список и итерируем
			new_games.reverse()
			for ng in new_games:
				# парсим инфу о новой игре
				nfo = sg.game_info(ng)

				# получаем список подписчиков бота
				subscriptions = db.get_subscriptions()

				# отправляем всем новость
				with open(sg.download_image(nfo["image"]), 'rb') as photo:
					for s in subscriptions:
						await bot.send_photo(
							s[1],
							photo,
							caption = nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" + nfo['link'],
							disable_notification = True
						)
				
				# обновляем ключ
				sg.update_lastkey(nfo['id'])


if __name__ == '__main__':
    dp.loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)
