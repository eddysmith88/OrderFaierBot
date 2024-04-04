from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.states import Form
from aiogram import exceptions

from datetime import date
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import re
from handlers.bot_messages import info
from keyboards.inline import inline_keyboard, inline_court, inline_edit, start_admin
from handlers.admin_panel import admin_start

from utils.data_base import Count, ClientBase, OrderList
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
    if message.from_user.id == 887934499:
        await message.answer(f'Адмін панель', reply_markup=start_admin)


@router.callback_query(lambda query: query.data == 'admin')
async def admin_callback(call: CallbackQuery):
    await admin_start(call.message)


@router.callback_query(lambda query: query.data == 'start')
async def start_menu(call: CallbackQuery, state: FSMContext):
    await start_choose(call.message, state)


async def start_choose(message: Message, state: FSMContext):
    await state.set_state(Form.select)
    order_lunch = session.query(Count).first().lunch
    order_soup = session.query(Count).first().soup
    buttons = []
    if order_lunch:
        buttons.append([InlineKeyboardButton(text='Обід 🥗', callback_data='обід')])
    if order_soup > 0:
        buttons.append([InlineKeyboardButton(text='Суп 🍲', callback_data='суп')])

    inline_order = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Що бажаєте замовити?", reply_markup=inline_order)


async def court(message: Message, state: FSMContext):
    """
    Перехід на кошик покупок
    :param message:
    :param state:
    :return:
    """
    await message.answer(f'У кошику:  🛒🛒🛒\n{await show_court(state)}')
    await message.answer(f'Замовити ще або завершити', reply_markup=inline_court)


async def show_court(state: FSMContext):
    """
    Кошик покупок
    :param state:
    :return:
    """
    data = await state.get_data()
    order_lunch = data.get('order_lunch')
    count_lunch = int(data.get('court_count_lunch', 0))
    order_soup = data.get('order_soup')
    count_soup = int(data.get('court_count_soup', 0))
    price_lunch = session.query(Count).first().price_lunch
    price_soup = session.query(Count).first().price_soup
    court_text = ""
    total_price = 0
    if order_lunch:
        total_lunch = count_lunch * price_lunch
        court_text += f"{order_lunch} - {count_lunch} x {price_lunch} = {total_lunch}\n"
        total_price += total_lunch
    if order_soup:
        total_soup = count_soup * price_soup
        court_text += f"{order_soup} - {count_soup} x {price_soup} = {total_soup}\n"
        total_price += total_soup
    return f'{court_text.strip()}\n\nДо сплати: {total_price} грн'


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


@router.callback_query(lambda query: query.data == 'back')
async def back(call: CallbackQuery, state: FSMContext):
    await court(call.message, state)


@router.callback_query(lambda query: query.data == 'next')
async def next_menu(call: CallbackQuery, state: FSMContext):
    await start_choose(call.message, state)


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
        await state.set_state(Form.court_count_lunch)
        await call.message.answer(f'Ви обрали ➡️➡️ {choice.capitalize()}\n\n'
                                  f'Введіть кількість, яку бажаєте замовити\n⬇️⬇️⬇️')
    elif choice == 'суп':
        if lunch_order.soup <= 0:
            await call.message.answer("На даний момент закінчились супи. Виберіть інший обід.")
            return
        await state.update_data(order_soup=choice)
        await state.set_state(Form.court_count_soup)
        await call.message.answer(f'Ви обрали ➡️➡️ {choice.capitalize()}\n\n'
                                  f'Введіть кількість, яку бажаєте замовити\n⬇️⬇️⬇️')


@router.message(Form.court_count_lunch)
async def form_count_lunch(message: Message, state: FSMContext):
    try:
        count = int(message.text)
        data = await state.get_data()
        lunch_order = session.query(Count).first()
        if count > lunch_order.lunch:
            await message.answer(f"Схоже ви хочете замовити більше ніж є в наявності.\n"
                                 f"Спробуйте замовити меншу кількість \n⬇️⬇️⬇️️")
            return
        await state.update_data(court_count_lunch=message.text)

        user = message.from_user.id

        client = session.query(ClientBase).filter_by(user_id=user).first()

        if client is None:
            await state.set_state(Form.phone_number)
            await message.answer('ведіть номер телефону \n'
                                 '⬇️⬇️⬇️')
        else:
            await court(message, state)
    except ValueError:
        await message.answer(f"Упсс... Вводьте будь ласка тільки цифри\n⬇️⬇️⬇️")


@router.message(Form.court_count_soup)
async def form_count_soup(message: Message, state: FSMContext):
    try:
        count = int(message.text)
        data = await state.get_data()
        soup_order = session.query(Count).first()
        if count > soup_order.soup:
            await message.answer(f"Схоже ви хочете замовити більше ніж є в наявності.\n"
                                 f"Спробуйте замовити меншу кількість \n⬇️⬇️⬇️️")
            return
        await state.update_data(court_count_soup=message.text)

        user = message.from_user.id

        client = session.query(ClientBase).filter_by(user_id=user).first()

        if client is None:
            await state.set_state(Form.phone_number)
            await message.answer('ведіть номер телефону в форматі 0931122333\n'
                                 '⬇️⬇️⬇️')
        else:
            await court(message, state)
    except ValueError:
        await message.answer(f"Упсс... Вводьте будь ласка тільки цифри\n⬇️⬇️⬇️")


@router.message(Form.phone_number)
async def form_phone_number(message: Message, state: FSMContext):
    """
    Форма для збереження номера телефона користувача
    :param message: Об'єкт, що представляє повідомлення від користувача
    :param state: Об'єкт для збереження стану конкретного користувача
    :return: None
    """
    phone_number = message.text.strip()
    data = await state.get_data()
    if not re.match(r'^0\d{9}$', phone_number):
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
    await court(message, state)


@router.callback_query(lambda query: query.data in ['comment', 'finish'])
async def handle_callback_query(call: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Функція, що обробляє callback-запити
    Розгалуження: Додати коментар чи закінчити покупку
    :param call: Об'єкт, що представляє повідомлення від користувача
    :param state: Об'єкт для збереження стану конкретного користувача
    :param bot:
    :return: None
    """
    data = await state.get_data()
    count_lunch = int(data.get('court_count_lunch', 0))
    count_soup = int(data.get('court_count_soup', 0))
    first_name = call.from_user.first_name
    last_name = call.from_user.last_name
    user_name = call.from_user.username
    current_date = date.today()
    formatted_date = current_date.strftime("%d.%m")
    create_test = OrderList(date=formatted_date, first_name=first_name, last_name=last_name, user_name=user_name, lunch=count_lunch,
                            soup=count_soup)
    session.add(create_test)
    session.commit()
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

    order_lunch = data.get('order_lunch')
    count_lunch = int(data.get('court_count_lunch', 0))
    order_soup = data.get('order_soup')
    count_soup = int(data.get('court_count_soup', 0))
    add_comment = data.get('add_comment', "")
    await (event.message if not is_message else event).answer(f'Ваше замовлення\n'
                                                              f' {order_lunch if order_lunch else ""} '
                                                              f'{count_lunch if count_lunch else ""}\n'
                                                              f'{order_soup if order_soup else ""} '
                                                              f'{count_soup if count_soup else ""}\n'
                                                              f'\n\nЧекаємо Вас приблизно о 12:00')

    user_id = (event.from_user.id if not is_message else event.from_user.id)

    client_base = session.query(ClientBase).filter_by(user_id=user_id).first()
    phone = client_base.phone if client_base else "Дані користувача не знайдені"
    user_id = client_base.user_id if client_base else "Не вдалося знайти user_id"
    lunch_order = session.query(Count).first()
    if lunch_order:
        if order_lunch == 'обід':
            lunch_order.lunch -= count_lunch
        if order_soup == 'суп':
            lunch_order.soup -= count_soup
        session.commit()
    oder_table = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Профіль', url=f'tg://user?id={event.from_user.id}')],
        [InlineKeyboardButton(text='Таблиця', callback_data='table')]
    ])
    await bot.send_message("@eddysmith_test", f'{event.from_user.full_name}\n\n'
                                              f'Замовив: {order_lunch if order_lunch else ""}: - {count_lunch if count_lunch else ""} шт\n'
                                              f'Замовив: {order_soup if order_soup else ""}: - {count_soup if count_soup else ""} шт \n\n'
                                              f'USER_ID {event.from_user.id}\n'
                                              f'Залишилось обідів: {lunch_order.lunch if lunch_order else "N/A"}\n'
                                              f'Залишилось супів {lunch_order.soup if lunch_order else "N/A"}\n\n'
                                              f'Додатковий коментар: \n\n{add_comment}',
                           reply_markup=oder_table)
    await info(event.message if not is_message else event)


@router.callback_query(lambda query: query.data == 'table')
async def get_table_callback(call: CallbackQuery, bot: Bot):
    """
    Коллбек для виводу таблиці з замовленнями
    :param call:
    :param bot:
    :return:
    """
    try:
        current_date = date.today()
        formatted_date = current_date.strftime("%d.%m")
        order_list = session.query(OrderList).filter(OrderList.date == formatted_date).all()

        message_text = ""
        for idx, order in enumerate(order_list, start=1):
            message_text += (f'{idx}. {order.first_name} {order.last_name} . {order.date}.  \n\n'
                             f'Lunch:    {order.lunch}      Soup:    {order.soup}  \n'
                             f'------------------------------------\n')

        await bot.send_message('@eddysmith_test', message_text)
    except exceptions.TelegramBadRequest as e:
        await bot.send_message('@eddysmith_test', 'На сьогодні замовлень немає')

