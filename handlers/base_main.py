from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.states import Form
import re
from handlers.bot_messages import info
from keyboards.inline import inline_keyboard, inline_order, inline_comment, inline_court, inline_edit

from utils.data_base import Count, ClientBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)
session = Session()


router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.select)

    await message.answer(f"Тут ви можете зробити замовлення\n"
                         f"просто слідуйте інструкціям", reply_markup=inline_keyboard)


@router.callback_query(lambda query: query.data == 'start')
async def start_menu(call: CallbackQuery, state: FSMContext):
    await start_choose(call.message, state)


async def start_choose(message: Message, state: FSMContext):
    await state.set_state(Form.select)
    await message.answer("Що бажаєте замовити?", reply_markup=inline_order)


async def court(message: Message, state: FSMContext):
    data = await state.get_data()
    order_lunch = data.get('order_lunch')
    count_lunch = int(data.get('court_count_lunch', 0))
    order_soup = data.get('order_soup')
    count_soup = int(data.get('court_count_soup', 0))
    await message.answer(f'У кошику:  🛒🛒🛒\n{order_lunch if order_lunch else ""} - {count_lunch if count_lunch else ""}\n\n'
                         f'{order_soup if order_soup else ""} - {count_soup if count_soup else ""}')
    await message.answer(f'Замовити ще або завершити', reply_markup=inline_court)


@router.callback_query(lambda query: query.data == 'edit_court')
async def edit_court(call: CallbackQuery):
    await call.message.answer('Редагувати кошик', reply_markup=inline_edit)


@router.callback_query(lambda query: query.data == 'minus_lunch')
async def minus_lunch(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count_lunch = int(data.get('court_count_lunch', 0))
    if count_lunch > 0:
        new_count = count_lunch - 1
        await state.update_data(court_count_lunch=new_count)
    await court(call.message, state)


@router.callback_query(lambda query: query.data == 'minus_soup')
async def minus_lunch(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count_soup = int(data.get('court_count_soup', 0))
    if count_soup > 0:
        new_count = count_soup - 1
        await state.update_data(court_count_soup=new_count)
    await court(call.message, state)


@router.callback_query(lambda query: query.data == 'next')
async def next_menu(call: CallbackQuery, state: FSMContext):
    await start_choose(call.message, state)

# @router.callback_query(lambda query: query.data in ['обід', 'суп'], Form.select)
# async def choose_order(call: CallbackQuery, state: FSMContext):
#     choice = call.data  # Отримуємо дані з інлайн-кнопки
#     if choice not in ['обід', 'суп']:
#         await call.answer("Невідома команда. Виберіть обід або суп.")
#         return
#
#     lunch_order = session.query(Count).first()
#     if choice == 'обід':
#         if lunch_order.lunch <= 0:
#             await call.message.answer("На даний момент закінчились ланчі. Виберіть інший обід.")
#             return
#         await state.update_data(order=choice)
#         # await state.set_state(Form.order_lunch)
#     elif choice == 'суп':
#         if lunch_order.soup <= 0:
#             await call.message.answer("На даний момент закінчились супи. Виберіть інший обід.")
#             return
#         await state.update_data(order=choice)
#         # await state.set_state(Form.order_soup)
#     await call.message.answer(f"Ви обрали ➡️➡️ {choice}")
#     await state.set_state(Form.count)
#     await call.message.answer(f'Введіть кількість, яку бажаєте замовити\n⬇️⬇️⬇️')
#
#
# async def court(call: CallbackQuery, state: FSMContext):
#     # data = await state.get_data()
#     # order = data.get('order')
#     # count = int(data.get('count', 0))
#     # await call.message.answer(f'У кошику: \n{order if order == "суп" else "none"} - {count}')
#     pass
#
#
# @router.callback_query(lambda query: query.data == 'done')
# async def done(call: CallbackQuery, state: FSMContext):
#     await call.message.answer('Бажаєте додати коментар до замовлення', reply_markup=inline_comment)
#
#
# @router.message(Form.count)
# async def form_count(message: Message, state: FSMContext, bot: Bot):
#     data = await state.get_data()
#     order = data.get('order')
#     count = int(data.get('count', 0))
#     if not message.text.isdigit():
#         await message.answer('Тільки цифри')
#         return
#     await state.update_data(count=message.text)
#
#     user = message.from_user.id
#
#     client = session.query(ClientBase).filter_by(user_id=user).first()
#
#     if client is None:
#         await state.set_state(Form.phone_number)
#         await message.answer('ведіть номер телефону \n'
#                              '⬇️⬇️⬇️')
#     else:
#         await message.answer('Бажаєте додати коментар до замовлення', reply_markup=inline_comment)


@router.callback_query(lambda query: query.data in ['обід', 'суп'], Form.select)
async def choose_order(call: CallbackQuery, state: FSMContext):
    choice = call.data
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
async def form_count_lunch(message: Message, state: FSMContext):
    data = await state.get_data()
    order_lunch = data.get('order_lunch')
    count_lunch = int(data.get('court_count_lunch', 0))
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    await state.update_data(court_count_lunch=message.text)

    user = message.from_user.id

    client = session.query(ClientBase).filter_by(user_id=user).first()

    if client is None:
        await state.set_state(Form.phone_number)
        await message.answer('ведіть номер телефону \n'
                             '⬇️⬇️⬇️')
    else:
        # await message.answer('Бажаєте додати коментар до замовлення', reply_markup=inline_court)
        await court(message, state)


@router.message(Form.court_count_soup)
async def form_count_soup(message: Message, state: FSMContext):
    data = await state.get_data()
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    await state.update_data(court_count_soup=message.text)

    user = message.from_user.id

    client = session.query(ClientBase).filter_by(user_id=user).first()

    if client is None:
        await state.set_state(Form.phone_number)
        await message.answer('ведіть номер телефону \n'
                             '⬇️⬇️⬇️')
    else:
        # await message.answer('Бажаєте додати коментар до замовлення', reply_markup=inline_court)
        await court(message, state)


@router.message(Form.phone_number)
async def form_phone_number(message: Message, state: FSMContext):
    phone_number = message.text.strip()

    # Перевірка формату телефонного номера
    if not re.match(r'^(0\d{9})$', phone_number):
        await message.answer('Невірно вказаний номер')
        return
    await state.update_data(phone_number=message.text)
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_name = message.from_user.username

    new_client = ClientBase(user_id=user_id, first_name=first_name, last_name=last_name, user_name=user_name,
                            phone=phone_number)
    session.add(new_client)
    session.commit()
    await message.answer('Бажаєте додати коментар до замовлення', reply_markup=inline_comment)


@router.callback_query(lambda query: query.data in ['comment', 'finish'])
async def handle_callback_query(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    count_lunch = int(data.get('court_count_lunch', 0))
    count_soup = int(data.get('court_count_soup', 0))
    sum_count = count_soup + count_lunch
    if call.data == 'comment':
        if sum_count <= 0:
            await call.message.answer('Кошик порожній. Зробіть замовлення')
            await court(call.message, state)
        else:
            await state.set_state(Form.add_comment)
            await call.message.answer(f'Напишіть ваш коментар\n⬇️⬇️⬇️')
    elif call.data == 'finish':
        if sum_count <= 0:
            await call.message.answer('Кошик порожній. Зробіть замовлення')
            await court(call.message, state)
        else:
            await state.update_data(add_comment="")
            await finalize_order(call, state, bot, is_message=False)


@router.message(Form.add_comment)
async def comment_form(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(add_comment=message.text)
    await finalize_order(message, state, bot, is_message=True)


async def finalize_order(event, state: FSMContext, bot: Bot, is_message: bool):
    data = await state.get_data()
    await state.clear()
    await (event.message if not is_message else event).answer(f'Ваше замовлення прийнято\n😃😃😃')

    # order = data.get('order')
    # count = int(data.get('count', 0))
    order_lunch = data.get('order_lunch')
    count_lunch = int(data.get('court_count_lunch', 0))
    order_soup = data.get('order_soup')
    count_soup = int(data.get('court_count_soup', 0))
    add_comment = data.get('add_comment', "")
    await (event.message if not is_message else event).answer(f'Вітаю ви замовили:\n'
                                                              f'➡️➡️ {order_lunch if order_lunch else "None"}\n'
                                                              f'{order_soup if order_soup else "None"}\n')

    user_id = (event.from_user.id if not is_message else event.from_user.id)

    client_base = session.query(ClientBase).filter_by(user_id=user_id).first()
    phone = client_base.phone if client_base else "Дані користувача не знайдені"
    user_id = client_base.user_id if client_base else "Не вдалося знайти user_id"
    lunch_order = session.query(Count).first()
    if lunch_order:
        if order_lunch == 'обід':
            lunch_order.lunch -= count_lunch
        elif order_soup == 'суп':
            lunch_order.soup -= count_soup
        session.commit()

    await bot.send_message("@eddysmith_test", f'Користувач {event.from_user.full_name}\n\n'
                                              f'Замовив: {order_lunch if order_lunch else ""}: - {count_lunch if count_lunch else ""} шт\n'
                                              f'Замовив: {order_soup if order_soup else ""}: - {count_soup if count_soup else ""} шт \n\nТелефон: {phone}\n\n'
                                              f'Залишилось обідів {lunch_order.lunch if lunch_order else "N/A"}\n\n'
                                              f'Залишилось супів {lunch_order.soup if lunch_order else "N/A"}\n\n'
                                              f'Додатковий коментар: \n\n{add_comment} ')
    await info(event.message if not is_message else event)
