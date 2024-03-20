from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="▶️▶️ Почати ▶️▶️", callback_data="start")],
])

inline_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обід 🥗', callback_data='обід')],
    [InlineKeyboardButton(text='Суп 🍲', callback_data='суп')]
])

inline_court = InlineKeyboardMarkup(inline_keyboard=[
    # [InlineKeyboardButton(text='Суп 🍲', callback_data='суп')],
    [InlineKeyboardButton(text='Замовити ще 🍲', callback_data='next')],
    [InlineKeyboardButton(text='Редагувати кошик 🥗', callback_data='edit_court')],
    [InlineKeyboardButton(text='Додати коментар до замовлення 🍳', callback_data='comment')],
    [InlineKeyboardButton(text='Завершити замовлення 🍽', callback_data='finish')]
])

inline_edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Видалити Обід 🥗', callback_data='minus_lunch')],
    [InlineKeyboardButton(text='Видалити Суп 🥗', callback_data='minus_soup')]
])


inline_comment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Додати коментар до замовлення 🍳', callback_data='comment')],
    [InlineKeyboardButton(text='Завершити замовлення 🍽', callback_data='finish')]
])

inline_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Додати обід 🥗', callback_data='add_lunch'),
     InlineKeyboardButton(text='Відняти обід 🥗', callback_data='remove_lunch'),
     InlineKeyboardButton(text='Обнулити обіди 🥗', callback_data='reset_lunch')
     ],
    [InlineKeyboardButton(text='Додати суп 🍲', callback_data='add_soup'),
     InlineKeyboardButton(text='Відянти суп 🍲', callback_data='remove_soup'),
     InlineKeyboardButton(text='Обнулити супи 🍲', callback_data='reset_soup')
     ],
    [InlineKeyboardButton(text='Показати кількість обідів 🥗', callback_data='show_lunch'),
     InlineKeyboardButton(text='Показати кількість супів 🍲', callback_data='show_soup')]
])
