import logging
from aiogram import Bot, Dispatcher, executor, types
import markups as nav # Сократил название, чтобы было удобнее
from db import Database


TOKEN = "5******3:A***************************4" # input my token

logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')

# Приветствие:
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if(not db.user_exists(message.from_user.id)): # Если наш пользователь еще не зарегистрирован, то выполняем регистрацию
        # Создаём нового пользователя:
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Укажите ваш ник")
    else: # Если уже зарегистрирован, то пишем сообщение и открываем ему меню!
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!", reply_markup=nav.mainMenu)

@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':  # Проверяем что мы в приватном режиме. РАБОТАЕТ ТОЛЬКО В ПРИВАТНОМ РЕЖИМЕ!
        if message.text == '👤 ПРОФИЛЬ':
            user_nickname = "Ваш ник: " + db.get_nickname(message.from_user.id)
            await bot.send_message(message.from_user.id, user_nickname)

        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if(len(message.text) > 15):
                    await bot.send_message(message.from_user.id, "Никнейм не должен превышать 15 символов")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, "Регистрация прошла успешно!", reply_markup=nav.mainMenu)
            else:
                await bot.send_message(message.from_user.id, "Не понятно что Вы ввели...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)