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


# scheduler.add_job(send_message_time, trigger="interval", seconds=5, args=(bot,'Приветики'))
# scheduler.add_job(send_message_time3, 'cron', day_of_week='mon-sun', hour=21, minute=16, end_date='2023-05-30', args=(bot,))
# @dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], content_types=["new_chat_members"], chat_id=config.ov_test_group_id)


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


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp)


