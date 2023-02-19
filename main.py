import logging
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import config
import jobs
import main
import messages
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sqlite_db

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot)
print("hello users")
try:
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    print("scheduler created")
except:
    print("scheduler creation failed")
finally:
    pass


keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
keyboard_back: InlineKeyboardMarkup = InlineKeyboardMarkup()

# Создаем объекты инлайн-кнопок
button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='ПРАВИЛА ЧАТА',
    callback_data='big_button_1_pressed')

button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='ПОЛЕЗНЫЕ ССЫЛКИ',
    callback_data='big_button_2_pressed')

button_3: InlineKeyboardButton = InlineKeyboardButton(
    text='ПОМОЩЬ ПО ГОРОДАМ',
    callback_data='big_button_3_pressed')

button_4: InlineKeyboardButton = InlineKeyboardButton(
    text='ЕЩЕ ИНФА',
    callback_data='big_button_4_pressed')

button_back: InlineKeyboardButton = InlineKeyboardButton(
    text='НАЗАД В МЕНЮ',
    callback_data='big_button_back_pressed')

# Добавляем кнопки в клавиатуру методом add
keyboard.add(button_1).add(button_2).add(button_3).add(button_4)
keyboard_back.add(button_back)

async def process_buttons_press(callback: CallbackQuery):
    await callback.answer()

# Этот хэндлер будет срабатывать на команду "/start" и отправлять в чат клавиатуру
async def process_start_command(message: Message):
    await message.answer(text='Привет, это инфо-бот чата "Отпускай Вещи!". Здесь мы собрали для тебя полезную информацию/'
                              ' и ссылки на ресурсы. Просто нажми на нужную кнопку!',
                         reply_markup=keyboard)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed'
async def process_button_1_press(callback: CallbackQuery):
    await callback.message.edit_text(messages.msg_dict.get('1'), reply_markup=keyboard_back, parse_mode="HTML")


async def process_button_2_press(callback: CallbackQuery):
    await callback.message.edit_text(messages.msg_dict.get('2'), reply_markup=keyboard_back, parse_mode="HTML")


async def process_button_3_press(callback: CallbackQuery):
    await callback.message.edit_text(messages.msg_dict.get('8'), reply_markup=keyboard_back, parse_mode = 'HTML')


async def process_button_4_press(callback: CallbackQuery):
    await callback.message.edit_text('тут надо еще инфы добавить', reply_markup=keyboard_back, parse_mode="HTML")


async def process_button_back_press(callback: CallbackQuery):
    await callback.message.edit_text('Нажми на кнопку для получения справки:', reply_markup=keyboard, parse_mode="HTML")

#
# Регистрируем хэндлер
dp.register_message_handler(process_start_command, chat_type=[types.ChatType.PRIVATE], commands='start')
dp.register_callback_query_handler(process_button_1_press,
                                   text='big_button_1_pressed')
dp.register_callback_query_handler(process_button_2_press,
                                   text='big_button_2_pressed')
dp.register_callback_query_handler(process_button_3_press,
                                   text='big_button_3_pressed')
dp.register_callback_query_handler(process_button_4_press,
                                   text='big_button_4_pressed')
dp.register_callback_query_handler(process_button_back_press,
                                   text='big_button_back_pressed')


async def autopost_message(bot: Bot, message_type: str):
    if sqlite_db.get_msg_id_by_type(int(message_type)) is None:
        msg = await bot.send_message(config.group_id, messages.msg_dict.get(message_type), parse_mode = 'HTML')
        sqlite_db.update_id_by_type(int(message_type), msg["message_id"])
    else:
        try:
            await bot.delete_message(config.group_id, sqlite_db.get_msg_id_by_type(int(message_type)))
        except:
            print('deletion error')
        msg = await bot.send_message(config.group_id, messages.msg_dict.get(message_type), parse_mode='HTML')
        sqlite_db.update_id_by_type(message_type, msg["message_id"])


scheduler.add_job(main.autopost_message, trigger="interval", seconds=30, args=(bot, '1'))
# scheduler.add_job(main.autopost_message, trigger="interval", seconds=200, args=(bot, '2'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='mon-sun', hour=8, minute=00, end_date='2023-05-30', args=(bot, '1'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='mon-sun', hour=20, minute=00, end_date='2023-05-30', args=(bot, '1'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='mon-sun', hour=14, minute=00, end_date='2023-05-30', args=(bot, '2'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='mon-sun', hour=10, minute=00, end_date='2023-05-30', args=(bot, '3'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='mon,wed,fri', hour=11, minute=00, end_date='2023-05-30', args=(bot, '4'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='tue', hour=11, minute=00, end_date='2023-05-30', args=(bot, '5'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='tue,thu,sat', hour=19, minute=00, end_date='2023-05-30', args=(bot, '6'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='wed,sun', hour=19, minute=30, end_date='2023-05-30', args=(bot, '7'))
    scheduler.add_job(autopost_message, 'cron', day_of_week='mon,wed,sat', hour=15, minute=00, end_date='2023-05-30', args=(bot, '8'))


async def on_startup(_):
    print('bot is online!')
    sqlite_db.sql_start()

if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


