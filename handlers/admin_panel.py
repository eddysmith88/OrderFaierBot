from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F, Bot
from filters.is_admin import IsAdmin
from keyboards.inline import inline_admin
from utils.states import Form
from aiogram.fsm.context import FSMContext
from utils.data_base import Count
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = Router()

engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)
session = Session()


@router.message(Command('admin'), IsAdmin(887934499))
async def admin_start(message: Message):
    await message.answer(f'Вітаю!\nЦе панель адміністратора\nОбери дію\n\n🔽🔽🔽🔽🔽', reply_markup=inline_admin)


@router.callback_query(lambda query: query.data in ['add_lunch', 'remove_lunch', 'reset_lunch', 'add_soup',
                                                    'remove_soup', 'reset_soup', 'show_lunch', 'show_soup'],
                       IsAdmin(887934499))
async def admin_choose(call: CallbackQuery, state: FSMContext):
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


@router.message(Form.lunch_remove)
async def lunch_remove(message: Message):
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    # Отримати поточне значення count з бази даних
    current_count = session.query(Count).first().lunch

    new_count = current_count - int(message.text)

    # Оновити значення count в базі даних
    session.query(Count).update({"lunch": new_count})
    session.commit()

    await message.answer(f'Кількість обідів оновлено: {new_count}\n🥗🍝🥧🍔🍕')
    await admin_start(message)


@router.message(Form.lunch_count)
async def lunch_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    # Отримати поточне значення count з бази даних
    current_count = session.query(Count).first().lunch

    # Змінити на нове значення а не додавання #TODO new count
    new_count = current_count + int(message.text)

    # Оновити значення count в базі даних
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
    # Отримати поточне значення soup з бази даних
    current_count_soup = session.query(Count).first().soup

    new_count_soup = current_count_soup - int(message.text)

    # Оновити значення soup в базі даних
    session.query(Count).update({"soup": new_count_soup})
    session.commit()

    await message.answer(f'Кількість супів оновлено: {new_count_soup}\n🍲🍲🍲')
    await admin_start(message)


@router.message(Form.soup_count)
async def lunch_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Тільки цифри')
        return
    # Отримати поточне значення soup з бази даних
    current_count_soup = session.query(Count).first().soup

    # Змінити на нове значення а не додавання
    new_count_soup = current_count_soup + int(message.text)

    # Оновити значення soup в базі даних
    session.query(Count).update({"soup": new_count_soup})
    session.commit()

    await state.update_data(soup_count=new_count_soup)
    await message.answer(f'Кількість супів оновлено: {new_count_soup}\n🍲🍲🍲')
    await admin_start(message)