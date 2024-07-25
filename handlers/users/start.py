from states.language_state import uz_state, ru_state
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, i18n
from keyboards.default.languages import lang_keyboard
_ = i18n.gettext


@dp.message_handler(CommandStart(), state=[uz_state, ru_state,])
async def bot_start(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Tilni tanlang", reply_markup=lang_keyboard)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Tilni tanlang", reply_markup=lang_keyboard)
