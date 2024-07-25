from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


pervous_button = InlineKeyboardButton(text="⏪ orqaga qaytish", callback_data="pervous")
next_button = InlineKeyboardButton(text="⏩ keyingi listga o'tish", callback_data="next")


pervous_button_img = InlineKeyboardButton(text="⏪ orqaga qaytish", callback_data="pervous_img")
next_button_img = InlineKeyboardButton(text="⏩ keyingi listga o'tish", callback_data="next_img")
menu_inline = InlineKeyboardButton(text="menu", callback_data="menu_call")