from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.inline import inline_keyboard


router = Router()


# INFO ABOUT BOT
@router.message(Command('info'))
async def info(message: Message):
    await message.answer(f'Вас вітає бот компанії FayerFamily (c) 👋\n\n'
                         f'Цей бот допомагає економити Ваш час 🕓⏳🐌\n'
                         f'В ньому Ви можете швидко забронювати обід, залишити певні коментарії ⌨️\n'
                         f'Також оплатити Ваше замовлення 💸\n\n'
                         f'Щоб зробити замовлення натисніть на цю кнопку', reply_markup=inline_keyboard)
