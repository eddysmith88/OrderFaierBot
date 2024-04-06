import asyncio
from aiogram import Bot, Dispatcher

from handlers import bot_messages, base_main, admin_panel
import config


async def main():
    bot = Bot(config.TOKEN)
    dp = Dispatcher()

    dp.include_routers(base_main.router, admin_panel.router, bot_messages.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
