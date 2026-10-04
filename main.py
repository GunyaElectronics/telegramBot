import asyncio
import os
import re
from datetime import datetime, timedelta
from typing import Optional, Tuple

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
    KeyboardButton
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests

def get_ukrainian_exchange_rates():
    # URL публічного API ПриватБанку для готівкового курсу
    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        data = response.json()
        
        rates = {}
        for item in data:
            # Зберігаємо лише основні валюти (наприклад, USD, EUR)
            rates[item['ccy']] = {
                'buy': float(item['buy']),
                'sale': float(item['sale'])
            }
        return rates
        
    except requests.exceptions.RequestException as e:
        print(f"Помилка при отриманні даних: {e}")
        return None


# Завантаження змінних з .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
MY_ID_RAW = os.getenv("MY_ID")

if not TOKEN or not MY_ID_RAW:
    raise ValueError("Необхідно вказати BOT_TOKEN та MY_ID у файлі .env")

MY_ID = int(MY_ID_RAW)


class MyBot:
    def __init__(self, token: str, my_id: int):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")
        self.my_id = my_id
        self._register_handlers()

    # --- Допоміжні методи ---
    def _parse_time_phrase(self, text: str) -> Tuple[Optional[datetime], str]:
        """
        Аналізує рядок і шукає відомі фрази часу на початку тексту.
        Повертає tuple: (datetime_об'єкт, залишок_тексту) або (None, text).
        """
        now = datetime.now()
        text = text.strip()

        patterns = [
            (r"^(через\s+)?(пів\s*години|півгодини)\s+(.*)", lambda m: (now + timedelta(minutes=30), m.group(3))),
            (r"^через\s+(\d+)\s+(хв|хвилину|хвилини|хвилин)\s+(.*)", lambda m: (now + timedelta(minutes=int(m.group(1))), m.group(3))),
            (r"^через\s+(\d+)\s+(год|годину|години|годин)\s+(.*)", lambda m: (now + timedelta(hours=int(m.group(1))), m.group(3))),
            (r"^через\s+(\d+)\s+(день|дні|днів)\s+(.*)", lambda m: (now + timedelta(days=int(m.group(1))), m.group(3))),
            (r"^завтра\s+(.*)", lambda m: (now + timedelta(days=1), m.group(1))),
            (r"^післязавтра\s+(.*)", lambda m: (now + timedelta(days=2), m.group(1))),
            (r"^(\d+)\s+(.*)", lambda m: (now + timedelta(minutes=int(m.group(1))), m.group(2))),
        ]

        for pattern, action in patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                return action(match)

        return None, text

    def _get_main_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Новини України"), KeyboardButton(text="Погода в Києві")],
                [KeyboardButton(text="📋 Мої нагадування"), KeyboardButton(text="💵 Курс валют")]
            ],
            resize_keyboard=True
        )

    def _get_reminder_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Виконано", callback_data="done"),
                InlineKeyboardButton(text="⏰ Відкласти на 15 хв", callback_data="snooze_15")
            ]
        ])

    async def _send_reminder(self, chat_id: int, text: str):
        await self.bot.send_message(
            chat_id,
            f"🔔 Нагадування: {text}",
            reply_markup=self._get_reminder_keyboard()
        )

    # --- Реєстрація обробників ---

    def _register_handlers(self):
        @self.dp.message(Command("start"), F.from_user.id == self.my_id)
        async def cmd_start(message: types.Message):
            await message.answer(
                "Привіт! Я твій персональний бот-нагадувальник.\n\n"
                "Можеш використовувати такі формати:\n"
                "• <code>/remind через 15 хвилин перевірити логі</code>\n"
                "• <code>/remind через 2 години зібрати стенд</code>\n"
                "• <code>/remind завтра написати скрипт</code>\n"
                "• <code>/remind пів години перерва на чай</code>\n"
                "• <code>/remind 10 перевірити завантаження</code>",
                parse_mode="HTML",
                reply_markup=self._get_main_keyboard()
            )

        @self.dp.message(F.text == "Новини України", F.from_user.id == self.my_id)
        async def cmd_news(message: types.Message):
            await message.answer("новина")

        @self.dp.message(F.text == "Погода в Києві", F.from_user.id == self.my_id)
        async def cmd_weather(message: types.Message):
            await message.answer("Зараз у Києві чудова погода! ☀️")

        @self.dp.message(F.text == "📋 Мої нагадування", F.from_user.id == self.my_id)
        async def cmd_my_reminders(message: types.Message):
            jobs = self.scheduler.get_jobs()
            if not jobs:
                await message.answer("📭 У вас немає запланованих нагадувань.")
                return

            response_lines = ["📋 <b>Ваші заплановані нагадування:</b>\n"]
            for idx, job in enumerate(jobs, start=1):
                text = job.kwargs.get("text", "Без опису")
                time_str = job.next_run_time.strftime("%d.%m.%Y %H:%M") if job.next_run_time else "Невідомий час"
                response_lines.append(f"{idx}. ⏰ <code>{time_str}</code> — {text}")

            await message.answer("\n".join(response_lines), parse_mode="HTML")

        # Ваш оновлений хендлер
        @self.dp.message(F.text == "💵 Курс валют", F.from_user.id == self.my_id)
        async def cmd_currency(message: types.Message):
            # Надсилаємо проміжний статус, оскільки запит до API може зайняти 1-2 секунди
            status_msg = await message.answer("🔄 Оновлюю дані...")
            
            # Отримуємо реальні дані
            actual_rates = get_ukrainian_exchange_rates()
            
            if actual_rates and actual_rates["USD"]["buy"] and actual_rates["EUR"]["buy"]:
                # Форматуємо виведення до двох знаків після коми
                usd_buy = f"{actual_rates['USD']['buy']:.2f}"
                usd_sell = f"{actual_rates['USD']['sale']:.2f}"
                eur_buy = f"{actual_rates['EUR']['buy']:.2f}"
                eur_sell = f"{actual_rates['EUR']['sale']:.2f}"
                
                text = (
                    "💵 <b>Актуальний курс валют (Приват Банк):</b>\n\n"
                    f"🇺🇸 <b>USD</b>: купівля {usd_buy} | продаж {usd_sell} грн\n"
                    f"🇪🇺 <b>EUR</b>: купівля {eur_buy} | продаж {eur_sell} грн"
                )
            else:
                # Резервний варіант, якщо API лежить
                text = (
                    "⚠️ Не вдалося отримати свіжі дані з API."
                )
                
            # Видаляємо повідомлення про завантаження та надсилаємо результат
            await status_msg.delete()
            await message.answer(text, parse_mode="HTML")

        @self.dp.message(Command("remind"), F.from_user.id == self.my_id)
        async def cmd_remind(message: types.Message, command: CommandObject):
            if not command.args:
                await message.answer(
                    "Помилка. Вкажи час та текст завдання.\n"
                    "Наприклад: <code>/remind завтра розібрати логі</code>",
                    parse_mode="HTML"
                )
                return

            run_date, task_text = self._parse_time_phrase(command.args)

            if not run_date:
                await message.answer("Не зміг розпізнати час. 🕒\nСпробуй: 'через 5 хвилин', 'завтра', 'пів години' тощо.")
                return

            if not task_text.strip():
                await message.answer("А що саме нагадати? Текст завдання порожній.")
                return

            self.scheduler.add_job(
                self._send_reminder,
                "date",
                run_date=run_date,
                kwargs={"chat_id": message.chat.id, "text": task_text.strip()}
            )

            await message.answer(f"✅ Нагадування встановлено на {run_date.strftime('%d.%m.%Y %H:%M')}.")

        @self.dp.callback_query(F.data == "done", F.from_user.id == self.my_id)
        async def process_done(callback: types.CallbackQuery):
            task_text = callback.message.text.replace("🔔 Нагадування: ", "")
            await callback.message.edit_text(
                text=f"✅ Виконано: {task_text}",
                reply_markup=None
            )
            await callback.answer("Відмічено як виконане!")

        @self.dp.callback_query(F.data == "snooze_15", F.from_user.id == self.my_id)
        async def process_snooze(callback: types.CallbackQuery):
            task_text = callback.message.text.replace("🔔 Нагадування: ", "")
            run_date = datetime.now() + timedelta(minutes=15)

            self.scheduler.add_job(
                self._send_reminder,
                "date",
                run_date=run_date,
                kwargs={"chat_id": callback.message.chat.id, "text": task_text}
            )

            await callback.message.edit_text(
                text=f"💤 Відкладено до {run_date.strftime('%H:%M')}: {task_text}",
                reply_markup=None
            )
            await callback.answer("Нагадування відкладено на 15 хвилин")

    # --- Запуск ---

    async def run(self):
        self.scheduler.start()
        await self.bot.delete_webhook(drop_pending_updates=True)
        print("Бот запущено...")
        await self.dp.start_polling(self.bot)


async def main():
    bot = MyBot(token=TOKEN, my_id=MY_ID)
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
