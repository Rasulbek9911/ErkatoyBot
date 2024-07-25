from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

lang_keyboard = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text='uz'),
            KeyboardButton(text='ru')
        ]

    ],
    resize_keyboard=True
)


back_keyboard = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text='Menu'),
        ]
    ],

    resize_keyboard=True
)
