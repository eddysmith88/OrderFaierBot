from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.states import Form
import re
from handlers.bot_messages import info
from keyboards.inline import inline_keyboard, inline_order, inline_comment, inline_court

from utils.data_base import Count, ClientBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)
session = Session()


router = Router()


@router.callback_query(lambda query: query.data in ['обід', 'суп'], Form.select)
async def choose_order(call: CallbackQuery, state: FSMContext):
    choice = call.data  # Отримуємо дані з інлайн-кнопки
    if choice not in ['обід', 'суп']:
        await call.answer("Невідома команда. Виберіть обід або суп.")
        return

    lunch_order = session.query(Count).first()
    if choice == 'обід':
        if lunch_order.lunch <= 0:
            await call.message.answer("На даний момент закінчились ланчі. Виберіть інший обід.")
            return
        await state.update_data(order_lunch=choice)
        # await state.set_state(Form.order_lunch)
        await state.set_state(Form.court_count_lunch)
        await call.message.answer(f'Введіть кількість, яку бажаєте замовити\n⬇️⬇️⬇️')
    elif choice == 'суп':
        if lunch_order.soup <= 0:
            await call.message.answer("На даний момент закінчились супи. Виберіть інший обід.")
            return
        await state.update_data(order_soup=choice)
        # await state.set_state(Form.order_soup)
        await state.set_state(Form.court_count_soup)
        await call.message.answer(f'Введіть кількість, яку бажаєте замовити\n⬇️⬇️⬇️')
    await call.message.answer(f"Ви обрали ➡️➡️ {choice}")
    # await state.set_state(Form.count)
    # await call.message.answer(f'Введіть кількість, яку бажаєте замовити\n⬇️⬇️⬇️')


@router.message(Form.court_count_lunch)
async def form_count_lunch(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    order_lunch = data.get('order_lunch')
    count_lunch = int(data.get('court_count_lunch', 0))
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    await state.update_data(court_count_lunch=message.text)
    await court(message, state)

    user = message.from_user.id

    client = session.query(ClientBase).filter_by(user_id=user).first()

    if client is None:
        await state.set_state(Form.phone_number)
        await message.answer('ведіть номер телефону \n'
                             '⬇️⬇️⬇️')
    else:
        await message.answer('Бажаєте додати коментар до замовлення', reply_markup=inline_court)


@router.message(Form.court_count_soup)
async def form_count_soup(message: Message, state: FSMContext):
    data = await state.get_data()
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    await state.update_data(court_count_soup=message.text)
    await court(message, state)

    user = message.from_user.id

    client = session.query(ClientBase).filter_by(user_id=user).first()

    if client is None:
        await state.set_state(Form.phone_number)
        await message.answer('ведіть номер телефону \n'
                             '⬇️⬇️⬇️')
    else:
        await message.answer('Бажаєте додати коментар до замовлення', reply_markup=inline_court)


async def court(event, state: FSMContext):
    data = await state.get_data()
    order_lunch = data.get('order_lunch')
    count_lunch = int(data.get('court_count_lunch', 0))
    order_soup = data.get('order_soup')
    count_soup = int(data.get('court_count_soup', 0))
    await event.message.answer(f'У кошику: \n{order_lunch} - {count_lunch}\n{order_soup} - {count_soup}')
    await event.message.answer(f'Замовити ще або завершити', reply_markup=inline_court)


    # откат
async def finalize_order(event, state: FSMContext, bot: Bot, is_message: bool):
    data = await state.get_data()
    await state.clear()
    await (event.message if not is_message else event).answer(f'Ваше замовлення прийнято\n😃😃😃')

    order = data.get('order')
    count = int(data.get('count', 0))
    add_comment = data.get('add_comment', "")
    await (event.message if not is_message else event).answer(f'Вітаю ви замовили:\n➡️➡️ {order}')

    user_id = (event.from_user.id if not is_message else event.from_user.id)

    client_base = session.query(ClientBase).filter_by(user_id=user_id).first()
    phone = client_base.phone if client_base else "Дані користувача не знайдені"
    user_id = client_base.user_id if client_base else "Не вдалося знайти user_id"

    lunch_order = session.query(Count).first()
    if lunch_order:
        if order == 'обід':
            lunch_order.lunch -= count
        elif order == 'суп':
            lunch_order.soup -= count
        session.commit()

    await bot.send_message("@eddysmith_test", f'Користувач {event.from_user.full_name}\n\n'
                                              f'Замовив: {order}: - {count} шт \n\nТелефон: {phone}\n\n'
                                              f'Залишилось обідів {lunch_order.lunch if lunch_order else "N/A"}\n\n'
                                              f'Залишилось супів {lunch_order.soup if lunch_order else "N/A"}\n\n'
                                              f'Додатковий коментар: \n\n{add_comment} ')
    await info(event.message if not is_message else event)