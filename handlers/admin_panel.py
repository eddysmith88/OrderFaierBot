from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, Bot
from filters.is_admin import IsAdmin
from keyboards.inline import inline_admin, channel_button
from utils.states import Form
from aiogram.fsm.context import FSMContext
from utils.data_base import Count
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = Router()

engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)
session = Session()


@router.message(Command('admin'), IsAdmin([887934499, 6706858065]))
async def admin_start(message: Message):
    """
    Функція, що оборобляє команду /admin і розпочинає дію з панеллю адміністратора
    :param message: Об'єкт, що представляє повідомлення від користувача.
    :return: None
    """
    await message.answer(f'Вітаю!\nЦе панель адміністратора\nОбери дію\n\n🔽🔽🔽🔽🔽', reply_markup=inline_admin)
    # count_data = Count(lunch=100, soup=50, price_lunch=10, price_soup=5)
    # session.add(count_data)
    # session.commit()


@router.callback_query(lambda query: query.data in ['add_lunch', 'remove_lunch', 'reset_lunch', 'add_soup',
                                                    'remove_soup', 'reset_soup', 'show_lunch', 'show_soup',
                                                    'price_lunch', 'price_soup'],
                       IsAdmin([887934499, 6706858065]))
async def admin_choose(call: CallbackQuery, state: FSMContext) -> None:
    """
    Функція, що обробляє callback-запити адміністратора та вибір доступних опцій
    :param call: Об'єкт, що представляє callback-запит від користувача
    :param state: Об'єкт для збереження стану конкретного користувача
    :return:
    """
    choice = call.data
    if choice == 'add_lunch':
        await call.message.answer(f'Скільки додати обідів?\n🥗🍝🥧🍔🍕\n🔽🔽🔽🔽🔽')
        await state.set_state(Form.lunch_count)
    elif choice == 'remove_lunch':
        await call.message.answer(f'Скільки відняти обідів?\n🥗🍝🥧🍔🍕n🔽🔽🔽🔽🔽')
        await state.set_state(Form.lunch_remove)
    elif choice == 'reset_lunch':
        await call.answer('Скинути обіди на 0')
        current_count_lunch = session.query(Count).first().lunch
        zero_count = current_count_lunch * 0
        session.query(Count).update({"lunch": zero_count})
        session.commit()
        await call.answer(f'Кількість обідів оновлено: {zero_count}\n🥗🍝🥧🍔🍕')
        await admin_start(call.message)
    elif choice == 'reset_soup':
        await call.answer('Скинути супи на 0')
        current_count_soup = session.query(Count).first().soup
        zero_count = current_count_soup * 0
        session.query(Count).update({"soup": zero_count})
        session.commit()
        await call.answer(f'Кількість cупів оновлено: {zero_count}\n🍲🍲🍲')
        await admin_start(call.message)
    elif choice == 'add_soup':
        await call.message.answer(f'Скільки додати супів?\n🍲🍲🍲\n🔽🔽🔽🔽🔽')
        await state.set_state(Form.soup_count)
    elif choice == 'remove_soup':
        await call.message.answer(f'Скільки відняти супів?\n🍲🍲🍲\n🔽🔽🔽🔽🔽')
        await state.set_state(Form.soup_remove)
    elif choice == 'show_lunch':
        current_count_lunch = session.query(Count).first().lunch
        await call.message.answer(f'Кількість обідів {current_count_lunch}\n🥗🍝🥧🍔🍕')
        await admin_start(call.message)
    elif choice == 'show_soup':
        current_count_soup = session.query(Count).first().soup
        await call.message.answer(f'Кількість супів\n🍲🍲🍲 {current_count_soup}')
        await admin_start(call.message)
    elif choice == 'price_lunch':
        await call.message.answer(f'Ціна на обід\n🍲🍲🍲\n🔽🔽🔽🔽🔽')
        await state.set_state(Form.price_lunch)
    elif choice == 'price_soup':
        await call.message.answer(f'Ціна на обід\n🍲🍲🍲\n🔽🔽🔽🔽🔽')
        await state.set_state(Form.price_soup)


@router.message(Form.price_lunch)
async def price_lunch(message: Message, state: FSMContext):
    """
    Функція, що зберігає стан price_lunch. Встановлює нове значення ціни
    :param message: Об'єкт, що представляє повідомлення від користувача
    :param state: Об'єкт для збереження стану конкретного користувача
    :return: None
    """
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    current_price = session.query(Count).first().price_lunch
    new_price = current_price * 0 + int(message.text)

    session.query(Count).update({"price_lunch": new_price})
    session.commit()

    await state.update_data(price_lunch=new_price)
    await message.answer(f'Ціна обіду оновлена: {new_price}\n🥗🍝🥧🍔🍕')
    await admin_start(message)


@router.message(Form.price_soup)
async def price_lunch(message: Message, state: FSMContext) -> None:
    """
    Функція, що зберігає стан price_soup. Встановлює нове значення ціни
    :param message: Об'єкт, що представляє повідомлення від користувача
    :param state: Об'єкт для збереження стану конкретного користувача
    :return: None
    """
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    current_price = session.query(Count).first().price_soup
    new_price = current_price * 0 + int(message.text)

    session.query(Count).update({"price_soup": new_price})
    session.commit()

    await state.update_data(price_soup=new_price)
    await message.answer(f'Ціна обіду оновлена: {new_price}\n🥗🍝🥧🍔🍕')
    await admin_start(message)


@router.callback_query(lambda query: query.data == 'today', IsAdmin([887934499, 6706858065]))
async def today_callback(call: CallbackQuery, state: FSMContext):
    """
    Функція, що обробляє callback-запит з панелі адміністратора
    :param call: Об'єкт, що представляє повідомлення від користувача
    :param state: Об'єкт для збереження стану конкретного користувача
    :return: None
    """
    await call.message.answer(f'Що сьогодні на обід \n⬇️⬇️⬇️')
    await state.set_state(Form.menu_text)


@router.message(Form.menu_text)
async def menu(message: Message, state: FSMContext, bot: Bot):
    """
    Функція приймає текст від адміністратора, і відправляє на канал
    :param message: Об'єкт, що представляє повідомлення від користувача
    :param state:
    :param bot:
    :return:
    """
    price_lunch = session.query(Count).first().price_lunch
    price_soup = session.query(Count).first().price_soup
    menu_text = message.text
    channel_id = -1001859713921
    channel_id_work = -1002048034204
    await bot.send_message(channel_id_work, f'Сьогодні в меню \n\n{menu_text}\n\n Ціна: {price_lunch} грн',
                           reply_markup=channel_button)


@router.message(Form.lunch_remove)
async def lunch_remove(message: Message):
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    current_count = session.query(Count).first().lunch
    new_count = current_count - int(message.text)

    session.query(Count).update({"lunch": new_count})
    session.commit()

    await message.answer(f'Кількість обідів оновлено: {new_count}\n🥗🍝🥧🍔🍕')
    await admin_start(message)


@router.message(Form.lunch_count)
async def lunch_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    current_count = session.query(Count).first().lunch
    new_count = current_count + int(message.text)

    session.query(Count).update({"lunch": new_count})
    session.commit()

    await state.update_data(lunch_count=new_count)
    await message.answer(f'Кількість обідів оновлено: {new_count}\n🥗🍝🥧🍔🍕')
    await admin_start(message)


@router.message(Form.soup_remove)
async def lunch_remove(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    current_count_soup = session.query(Count).first().soup
    new_count_soup = current_count_soup - int(message.text)

    session.query(Count).update({"soup": new_count_soup})
    session.commit()

    await message.answer(f'Кількість супів оновлено: {new_count_soup}\n🍲🍲🍲')
    await admin_start(message)


@router.message(Form.soup_count)
async def lunch_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return

    current_count_soup = session.query(Count).first().soup
    new_count_soup = current_count_soup + int(message.text)

    session.query(Count).update({"soup": new_count_soup})
    session.commit()

    await state.update_data(soup_count=new_count_soup)
    await message.answer(f'Кількість супів оновлено: {new_count_soup}\n🍲🍲🍲')
    await admin_start(message)
