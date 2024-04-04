from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.inline import inline_keyboard, channel_button
from aiogram.enums.chat_type import ChatType
import asyncio


router = Router()


@router.message(Command('info'))
async def info(message: Message):
    await message.answer(f'Вітаємо! 👋\n\n'
                         f'Цей бот допомагає економити Ваш час 🕓⏳🐌\n'
                         f'В ньому Ви можете швидко забронювати обід та залишити певні коментарі до замовлення ⌨️\n'
                         f'Наприклад якщо хочете забронювати щось окрім обіду, напишіть це в коментарі до замовлення\n\n'
                         f'Щоб замовити натисніть на цю кнопку', reply_markup=inline_keyboard)


@router.channel_post()
async def channel_post(message: Message, bot: Bot):
    if message.chat.type == ChatType.CHANNEL:
        await bot.send_message(message.chat.id, 'Щоб замовити натисніть сюди', reply_markup=channel_button)
        await message.answer(f'ID CHAT {message.chat.id}')
        delete_delay = 5
        await asyncio.sleep(delete_delay)
        if message.from_user.id != 887934499:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await asyncio.sleep(1)


