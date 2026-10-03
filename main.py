import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# Завантажуємо змінні з файлу .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_ID = os.getenv("MY_ID")

# Перевірка, чи всі змінні на місці
if not BOT_TOKEN or not MY_ID:
    raise ValueError("Необхідно вказати BOT_TOKEN та MY_ID у файлі .env")

# Перетворюємо ID на число, оскільки Telegram ID є цілим числом
MY_ID = int(MY_ID)

# Налаштування логування для зручного відстеження подій у консолі
logging.basicConfig(level=logging.INFO)

# Ініціалізуємо бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хендлер для команди /start
# Магічний фільтр F.from_user.id == MY_ID гарантує, що код виконається ТІЛЬКИ для вас
@dp.message(CommandStart(), F.from_user.id == MY_ID)
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Я твій приватний помічник. Система запущена і готова до роботи. 🚀")

# Хендлер для будь-яких інших текстових повідомлень (проста дія: ехо-відповідь)
@dp.message(F.text, F.from_user.id == MY_ID)
async def echo(message: types.Message):
    await message.answer(f"Я отримав твоє повідомлення: {message.text}")

async def main():
    print("Бот запускається...")
    # Видаляємо всі оновлення, які могли накопичитися, поки бот був вимкнений
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаємо процес отримання оновлень (Long Polling)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запуск асинхронного циклу подій
    asyncio.run(main())