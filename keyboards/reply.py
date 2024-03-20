from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="lunch"), KeyboardButton(text="soup")
        ]
    ],
    resize_keyboard=True,  # Розмір клавіатури
    one_time_keyboard=True,  # Приховує клавіатуру
    input_field_placeholder='Choose a function',  # Плейсходер
    selective=True  # Відображає клавіатуру в того хто її викликав
)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add lunch"), KeyboardButton(text="Add soup")],
    [KeyboardButton(text="Remove lunch"), KeyboardButton(text="Remove soup")],
    [KeyboardButton(text="Reset lunch"), KeyboardButton(text="Reset soup")]
], resize_keyboard=True, one_time_keyboard=True, selective=True, )

comment = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="додати"), (KeyboardButton(text='Непотрібно'))]
], input_field_placeholder='Додати коментар', selective=True, resize_keyboard=True)


rmk = ReplyKeyboardRemove()
