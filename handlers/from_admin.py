from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F, Bot
from filters.is_admin import IsAdmin
from keyboards.reply import admin_keyboard, rmk
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
async def admin(message: Message):
    await message.answer('Choose an action:', reply_markup=admin_keyboard)


@router.message(F.text == "Add lunch")
async def add_lunch(message: Message, state: FSMContext):
    await message.answer('How many lunches do you want to add?', reply_markup=rmk)
    await state.set_state(Form.lunch_count)


@router.message(F.text == "Remove lunch")
async def remove_lunch(message: Message, state: FSMContext):
    await message.answer('How many lunches do you want to remove?', reply_markup=rmk)
    await state.set_state(Form.lunch_remove)


@router.message(F.text == "Add soup")
async def add_soup(message: Message, state: FSMContext):
    await message.answer('How many soups do you want to add?', reply_markup=rmk)
    await state.set_state(Form.soup_count)


@router.message(F.text == "Remove soup")
async def remove_soup(message: Message, state: FSMContext):
    await message.answer('How many soup do you want to remove', reply_markup=rmk)
    await state.set_state(Form.soup_remove)


@router.message(F.text == "Reset lunch")
async def reset_lunch(message: Message):
    # TODO Спробувати зробити підтвердження
    await message.answer('Скинути на 0', reply_markup=rmk)
    current_count_lunch = session.query(Count).first().lunch
    zero_count = current_count_lunch * 0
    session.query(Count).update({"lunch": zero_count})
    session.commit()
    await message.answer(f'Кількість обідів оновлено: {zero_count}')
    await admin(message)


@router.message(F.text == "Reset soup")
async def reset_lunch(message: Message):
    await message.answer('Скинути на 0', reply_markup=rmk)
    current_count_soup = session.query(Count).first().soup
    zero_count = current_count_soup * 0
    session.query(Count).update({"soup": zero_count})
    session.commit()
    await message.answer(f'Кількість cупів оновлено: {zero_count}')
    await admin(message)


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

    await message.answer(f'Кількість обідів оновлено: {new_count}')
    await admin(message)


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
    await message.answer(f'Кількість обідів оновлено: {new_count}')
    await admin(message)


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

    await message.answer(f'Кількість супів оновлено: {new_count_soup}')
    await admin(message)


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
    await message.answer(f'Кількість супів оновлено: {new_count_soup}')
    await admin(message)





