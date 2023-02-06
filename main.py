import logging
import time
from aiogram import Bot, Dispatcher, executor, types
import config
import messages
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


async def send_message_time(bot: Bot, text_message):
    await bot.send_message(config.group_id, text_message, parse_mode='HTML')


# scheduler.add_job(send_message_time, trigger="interval", minutes=60, args=(bot,'Я уже на сервере! Присылаю приветики каждый час!'))
# scheduler.add_job(send_message_time, 'cron', day_of_week='mon-sun', hour=19, minute=25, end_date='2023-05-30', args=(bot, 'Это сообщение приходит каждый день в 19:25'))
scheduler.add_job(send_message_time, 'cron', day_of_week='mon-sun', hour=8, minute=00, end_date='2023-05-30', args=(bot, messages.message1))
scheduler.add_job(send_message_time, 'cron', day_of_week='mon-sun', hour=20, minute=00, end_date='2023-05-30', args=(bot, messages.message1))
scheduler.add_job(send_message_time, 'cron', day_of_week='mon-sun', hour=14, minute=00, end_date='2023-05-30', args=(bot, messages.message2))
scheduler.add_job(send_message_time, 'cron', day_of_week='mon-sun', hour=10, minute=00, end_date='2023-05-30', args=(bot, messages.message3))
scheduler.add_job(send_message_time, 'cron', day_of_week='mon,wed,fri', hour=11, minute=00, end_date='2023-05-30', args=(bot, messages.message4))
scheduler.add_job(send_message_time, 'cron', day_of_week='tue', hour=11, minute=00, end_date='2023-05-30', args=(bot, messages.message5))
scheduler.add_job(send_message_time, 'cron', day_of_week='tue,thu,sat', hour=19, minute=00, end_date='2023-05-30', args=(bot, messages.message6))
scheduler.add_job(send_message_time, 'cron', day_of_week='wed,sun', hour=19, minute=30, end_date='2023-05-30', args=(bot, messages.message7))
scheduler.add_job(send_message_time, 'cron', day_of_week='mon,wed,sat', hour=15, minute=00, end_date='2023-05-30', args=(bot, messages.message8))

@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], content_types=["new_chat_members"], chat_id=config.group_id)
async def new_member(message):
    name = message.new_chat_members[0].username
    await bot.send_message(message.chat.id, '@' + name + ', здарова!', parse_mode='HTML')


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name} {time.asctime()}')
    await message.reply('Привет, @' + user_name + '!')


@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['help'])
async def help_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    print(bot.get_chat)
    logging.info(f'{user_id=} {user_full_name} {time.asctime()}')
    await message.answer("Вот список команд, которые я умею выполнять:")


@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def help_handler(message: types.Message):
    if message.text == '1':
        await message.answer(messages.message1, parse_mode='HTML')
    if message.text == '2':
        await message.answer(messages.message2, parse_mode='HTML')
    if message.text == '3':
        await message.answer(messages.message3, parse_mode='HTML')
    if message.text == '4':
        await message.answer(messages.message4, parse_mode='HTML')
    if message.text == '5':
        await message.answer(messages.message5, parse_mode='HTML')
    if message.text == '6':
        await message.answer(messages.message6, parse_mode='HTML')
    if message.text == '7':
        await message.answer(messages.message7, parse_mode='HTML')
    if message.text == '8':
        await message.answer(messages.message8, parse_mode='HTML')
    else:
        pass


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp)


