from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    select = State()  # 1
    phone_number = State()  # 1
    # count = State()
    # order = State()
    lunch_count = State()  # 1
    lunch_remove = State()  # 1
    soup_count = State()  # 1
    soup_remove = State()  # 1
    # finish_state = State()
    add_comment = State()  # 1
    # comment = State()
    order_lunch = State()  # 1
    order_soup = State()  # 1
    court_count_lunch = State()  # 1
    court_count_soup = State()  # 1
    menu_text = State()  # 1
    price_lunch = State()  # 1
    price_soup = State()  # 1

