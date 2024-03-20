import asyncio
from aiogram import Bot, Dispatcher

from handlers import bot_messages, base_main, from_admin, admin_panel


async def main():
    bot = Bot('6497402892:AAFCF0IGPevTp0mqIewRNilGMXXr0UW-XZA')
    dp = Dispatcher()

    dp.include_routers(base_main.router, admin_panel.router, bot_messages.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
