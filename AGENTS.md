# AGENTS.md

## Project Overview
A private Telegram bot built with `aiogram`. It responds to `/start` and echoes back text messages, but *only* to the user specified by `MY_ID` in the `.env` file. 

## Critical Setup & Runtime
- **Environment Variables**: Requires `BOT_TOKEN` and `MY_ID` in a `.env` file.
- **Running the bot**: `python main.py`
- **Debugging**: Use the "Python Debugger: Current File" configuration in VS Code (targets `main.py`).
- **Dependency Management**: Uses `aiogram` and `python-dotenv`. (Verify current environment for exact versioning/installation requirements).

## Architecture & Flow
- **Entry Point**: `main.py`
- **Main Execution**: `asyncio.run(main())` inside `if __name__ == "__main__":`.
- **Core Logic**:
    - Uses `aiogram`'s `Dispatcher` and `Bot`.
    - Employs `F` (Magic Filter) for user-specific access control (`F.from_user.id == MY_ID`).
    - `bot.delete_webhook(drop_pending_updates=True)` is called at startup to prevent message spamming after being offline.
- **Logging**: Configured to `INFO` level on standard output.

## Code Style & Conventions
- **Typing**: Strict type hinting is mandatory. Always import types from `aiogram.types` (e.g., `Message`, `CallbackQuery`).
- **Formatting**: Adhere to PEP-8. It is recommended to use `black` and `ruff` for code formatting and linting.
- **Asynchronous Programming**: Never use blocking synchronous code inside handlers. Always use `async`/`await` and non-blocking libraries (e.g., `aiohttp` instead of `requests`).
- **Docstrings**: Provide brief docstrings for any complex logic or new utility functions to maintain readability.

## Project Structure & Scalability Recommendations
While currently contained within `main.py`, future feature expansions should follow these architectural guidelines:
- **Routers**: Use `aiogram`'s `Router` system instead of attaching everything to the main `Dispatcher`. Group handlers logically (e.g., `handlers/user.py`, `handlers/admin.py`).
- **Configuration**: If the configuration grows beyond two variables, migrate from raw `os.getenv` to `pydantic-settings` for robust validation.
- **UI Components**: Keep keyboards (`ReplyKeyboardMarkup`, `InlineKeyboardMarkup`) in separate modules (e.g., `keyboards/`) to prevent cluttering handler files.

## AI Agent Instructions (Development Rules)
1. **Privacy First**: When adding *any* new handler, ensure the `F.from_user.id == MY_ID` filter (or an equivalent middleware) is applied to maintain the bot's private nature.
2. **Version Awareness**: This project uses `aiogram` 3.x. Do not generate code using `aiogram` 2.x syntax (e.g., avoid `@dp.message_handler()`, use `@dp.message()` instead).
3. **Graceful Shutdown**: When modifying the startup/shutdown logic, ensure the bot session closes properly to avoid `asyncio` unclosed client session warnings.