from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    # TODO Прибрати лишні
    select = State()
    phone_number = State()
    count = State()
    order = State()
    lunch_count = State()
    lunch_remove = State()
    soup_count = State()
    soup_remove = State()
    finish_state = State()
    add_comment = State()
    comment = State()
    order_lunch = State()
    order_soup = State()
    court_count_lunch = State()
    court_count_soup = State()


