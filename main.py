import asyncio
import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Завантаження змінних з .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
MY_ID = int(os.getenv("MY_ID"))

if not TOKEN or not MY_ID:
    raise ValueError("Необхідно вказати BOT_TOKEN та MY_ID у файлі .env")

# Ініціалізація
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone='Europe/Kyiv')

def parse_time_phrase(text: str):
    """
    Аналізує рядок і шукає відомі фрази часу на початку тексту.
    Повертає tuple: (datetime_об'єкт, залишок_тексту) або (None, text).
    """
    now = datetime.now()
    text = text.strip()

    # Словник регулярних виразів та функцій для обчислення часу.
    # Порядок має значення: від найбільш специфічних до найпростіших.
    patterns = [
        # (через) пів години / півгодини
        (r'^(через\s+)?(пів\s*години|півгодини)\s+(.*)', lambda m: (now + timedelta(minutes=30), m.group(3))),
        # через X хвилин
        (r'^через\s+(\d+)\s+(хв|хвилину|хвилини|хвилин)\s+(.*)', lambda m: (now + timedelta(minutes=int(m.group(1))), m.group(3))),
        # через X годин
        (r'^через\s+(\d+)\s+(год|годину|години|годин)\s+(.*)', lambda m: (now + timedelta(hours=int(m.group(1))), m.group(3))),
        # через X днів
        (r'^через\s+(\d+)\s+(день|дні|днів)\s+(.*)', lambda m: (now + timedelta(days=int(m.group(1))), m.group(3))),
        # завтра
        (r'^завтра\s+(.*)', lambda m: (now + timedelta(days=1), m.group(1))),
        # післязавтра
        (r'^післязавтра\s+(.*)', lambda m: (now + timedelta(days=2), m.group(1))),
        # просто число (хвилини - для сумісності з попереднім форматом)
        (r'^(\d+)\s+(.*)', lambda m: (now + timedelta(minutes=int(m.group(1))), m.group(2))),
    ]

    # Проходимось по патернах, шукаючи збіг на початку рядка
    for pattern, action in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            return action(match)

    return None, text

# Створення клавіатури з кнопками
def get_reminder_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Виконано", callback_data="done"),
            InlineKeyboardButton(text="⏰ Відкласти на 15 хв", callback_data="snooze_15")
        ]
    ])

# Функція, яку викликає планувальник
async def send_reminder(chat_id: int, text: str):
    await bot.send_message(
        chat_id, 
        f"🔔 Нагадування: {text}",
        reply_markup=get_reminder_keyboard()
    )

@dp.message(Command("start"), F.from_user.id == MY_ID)
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я твій персональний бот-нагадувальник.\n\n"
        "Можеш використовувати такі формати:\n"
        "• <code>/remind через 15 хвилин перевірити логі</code>\n"
        "• <code>/remind через 2 години зібрати стенд</code>\n"
        "• <code>/remind завтра написати скрипт</code>\n"
        "• <code>/remind пів години перерва на чай</code>\n"
        "• <code>/remind 10 перевірити завантаження</code>",
        parse_mode="HTML"
    )

@dp.message(Command("remind"), F.from_user.id == MY_ID)
async def cmd_remind(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("Помилка. Вкажи час та текст завдання.\nНаприклад: <code>/remind завтра розібрати логі</code>", parse_mode="HTML")
        return

    # Передаємо весь текст після /remind у наш парсер
    run_date, task_text = parse_time_phrase(command.args)

    if not run_date:
        await message.answer("Не зміг розпізнати час. 🕒\nСпробуй: 'через 5 хвилин', 'завтра', 'пів години' тощо.")
        return

    if not task_text.strip():
        await message.answer("А що саме нагадати? Текст завдання порожній.")
        return

    scheduler.add_job(
        send_reminder,
        "date",
        run_date=run_date,
        kwargs={"chat_id": message.chat.id, "text": task_text.strip()}
    )

    await message.answer(f"✅ Нагадування встановлено на {run_date.strftime('%d.%m.%Y %H:%M')}.")

# --- ОБРОБНИКИ КНОПОК ---

@dp.callback_query(F.data == "done", F.from_user.id == MY_ID)
async def process_done(callback: types.CallbackQuery):
    task_text = callback.message.text.replace("🔔 Нагадування: ", "")
    
    await callback.message.edit_text(
        text=f"✅ Виконано: {task_text}",
        reply_markup=None
    )
    await callback.answer("Відмічено як виконане!")

@dp.callback_query(F.data == "snooze_15", F.from_user.id == MY_ID)
async def process_snooze(callback: types.CallbackQuery):
    task_text = callback.message.text.replace("🔔 Нагадування: ", "")
    
    run_date = datetime.now() + timedelta(minutes=15)
    
    scheduler.add_job(
        send_reminder,
        "date",
        run_date=run_date,
        kwargs={"chat_id": callback.message.chat.id, "text": task_text}
    )
    
    await callback.message.edit_text(
        text=f"💤 Відкладено до {run_date.strftime('%H:%M')}: {task_text}",
        reply_markup=None
    )
    await callback.answer("Нагадування відкладено на 15 хвилин")

async def main():
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True) 
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())