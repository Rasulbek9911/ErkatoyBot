from loader import dp, bot
from aiogram import types
import requests
import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from states.language_state import uz_state, ru_state
import bleach
from keyboards.default.languages import back_keyboard
from keyboards.inline.inlines_key import pervous_button, next_button, pervous_button_img, next_button_img
from aiogram.dispatcher import FSMContext
from data.config import DOMAIN


@dp.message_handler(text="ru")
async def lang_select(msg: types.Message):
    res = requests.get(f"{DOMAIN}category/",
                       params={"lang": "ru", },)
    print(res.json())
    category_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in res.json():
        category_keyboard.insert(i["name_ru"])
    await ru_state.ru1.set()
    await msg.answer("Rus tilini tanladingiz", reply_markup=category_keyboard)


def sanitize_html(html_content):
    if html_content is None:
        return html_content
    allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS)
    cleaned_content = bleach.clean(html_content, tags=allowed_tags, strip=True)
    cleaned_content = cleaned_content.replace('<p>', '').replace('</p>', '\n')
    cleaned_content = cleaned_content.replace('&nbsp;', ' ')
    cleaned_content = cleaned_content.replace('&ndash;', ' ')
    cleaned_content = cleaned_content.replace('&lsquo;', ' ')
    cleaned_content = cleaned_content.replace('&ldquo;', ' ')
    cleaned_content = cleaned_content.replace('&rdquo;', ' ')
    cleaned_content = cleaned_content.replace(
        '&laquo;', '').replace('&raquo;', '')
    return cleaned_content


def remove_non_breaking_spaces(text):
    return text.replace('&nbsp;', '')


@dp.message_handler(text='Orqaga', state=[ru_state.ru1, ru_state.ru2])
async def back_def(msg: types.Message, state: FSMContext):

    current_state = await state.get_state()

    if current_state == "uz_state:uz2":

        category_text = await state.get_data('category_text')

        res = requests.get(f"{DOMAIN}content/",
                           params={"msg": category_text['category_text'], 'lang': 'uz'},)
        content = res.json()
        print(content)
        text = ""
        inline_ertaklar = types.InlineKeyboardMarkup(row_width=5)
        for index, i in enumerate(content['results']):
            text += f"{index+1}. {i['title']}\n"
            inline_ertaklar.insert(types.InlineKeyboardButton(
                text=f"{index + 1}", callback_data=i['id']))

        if content['next'] is not None:
            inline_ertaklar.add(next_button)
        elif content['previous'] is not None:
            inline_ertaklar.add(pervous_button)
        await uz_state.uz1.set()
        await msg.answer(text, reply_markup=inline_ertaklar)
    if current_state == 'uz_state:uz1':
        res = requests.get(f"{DOMAIN}category/",
                           params={"lang": "uz", },)
        category_keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=2)
        for i in res.json():
            category_keyboard.insert(i["name_uz"])
        await msg.answer("Uzbek tilini tanladingiz", reply_markup=category_keyboard)


@dp.message_handler(state=ru_state.ru1)
async def lang_select(msg: types.Message, state: FSMContext):
    res = requests.get(f"{DOMAIN}content/",
                       params={"msg": msg.text, 'lang': "ru"},)
    await state.update_data(category_text=msg.text)

    content = res.json()
    print(content)
    if content['msg']:
        await msg.answer("В этой категории нет информации")
        return
    await state.update_data(next_url=content['next'])
    await state.update_data(previous_url=content['previous'])
  
    if len(content['results']) == 0:
        await msg.answer("В этой категории нет информации")
    elif content['results'][0]['rasm']:
        inline_ertaklar = types.InlineKeyboardMarkup(row_width=4)
        text = ""
        for index, i in enumerate(content['results']):
            text += f"{index+1}. {i['id']}\n"
            inline_ertaklar.insert(types.InlineKeyboardButton(
                text=f"{index + 1}", callback_data=i['id']))
        text += "\n"
        if content['next'] is not None:
            inline_ertaklar.add(next_button_img)
        elif content['previous'] is not None:
            inline_ertaklar.add(pervous_button_img)

        media = types.MediaGroup()

        for i in content['results']:
            photo = types.InputFile(
                path_or_bytesio=f"/home/rasulbek/PycharmProjects/mukammal-bot-paid/erkatoy_django{i['rasm']}")
            media.attach_photo(photo)
        await msg.answer(".", reply_markup=ReplyKeyboardRemove())
        await msg.reply_media_group(media=media)
        await msg.answer(text, reply_markup=inline_ertaklar)
    else:
        text = ""
        inline_ertaklar = types.InlineKeyboardMarkup(row_width=5)
        for index, i in enumerate(content['results']):
            text += f"{index+1}. {i['title']}\n"
            inline_ertaklar.insert(types.InlineKeyboardButton(
                text=f"{index + 1}", callback_data=i['id']))
        text += "\n"
        if content['next'] is not None:
            inline_ertaklar.add(next_button)
        elif content['previous'] is not None:
            inline_ertaklar.add(pervous_button)

        await uz_state.uz2.set()
        await msg.answer(".", reply_markup=ReplyKeyboardRemove())
        await msg.answer(text, reply_markup=inline_ertaklar)


@dp.callback_query_handler(text="next_img", state=[ru_state.ru1, ru_state.ru2])
async def next_handler(call: types.CallbackQuery, state: FSMContext):
    next_url = await state.get_data('next_url')

    res = requests.get(next_url['next_url'])
    content = res.json()

    await state.update_data(next_url=content['next'])
    await state.update_data(previous_url=content['previous'])
    inline_ertaklar = types.InlineKeyboardMarkup(row_width=4)
    text = ""
    for index, i in enumerate(content['results']):
        text += f"{index+1}. {i['id']}\n"
        inline_ertaklar.insert(types.InlineKeyboardButton(
            text=f"{index + 1}", callback_data=i['id']))
    text += "\n"
    if content['next'] is not None:
        inline_ertaklar.add(next_button_img)
    elif content['previous'] is not None:
        inline_ertaklar.add(pervous_button_img)

    media = types.MediaGroup()

    for i in content['results']:
        photo = types.InputFile(
            path_or_bytesio=f"/home/rasulbek/PycharmProjects/mukammal-bot-paid/erkatoy_django{i['rasm']}")
        media.attach_photo(photo)
    await call.answer(".", reply_markup=ReplyKeyboardRemove())
    await call.message.answer_media_group(media=media)
    await call.answer(text, reply_markup=inline_ertaklar)


@dp.callback_query_handler(text="next", state=[ru_state.ru1, ru_state.ru2])
async def next_handler(call: types.CallbackQuery, state: FSMContext):
    next_url = await state.get_data('next_url')

    res = requests.get(next_url['next_url'])
    content = res.json()

    await state.update_data(next_url=content['next'])
    await state.update_data(previous_url=content['previous'])
    text = ""
    inline_ertaklar = types.InlineKeyboardMarkup(row_width=5)
    for index, i in enumerate(content['results']):
        text += f"{index+1}. {i['title']}\n"
        inline_ertaklar.insert(types.InlineKeyboardButton(
            text=f"{index + 1}", callback_data=i['id']))

    if content['next'] is not None:
        inline_ertaklar.add(next_button)
    elif content['previous'] is not None:
        inline_ertaklar.add(pervous_button)
    await call.message.delete()
    await call.message.answer(text, reply_markup=inline_ertaklar)


@dp.callback_query_handler(text="pervous", state=[ru_state.ru1, ru_state.ru2])
async def pervous_handler(call: types.CallbackQuery, state: FSMContext):

    previous_url = await state.get_data('previous_url')

    res = requests.get(previous_url['previous_url'])
    content = res.json()

    await state.update_data(next_url=content['next'])
    await state.update_data(previous_url=content['previous'])
    text = ""
    inline_ertaklar = types.InlineKeyboardMarkup(row_width=5)
    for index, i in enumerate(content['results']):
        text += f"{index+1}. {i['title']}\n"
        inline_ertaklar.insert(types.InlineKeyboardButton(
            text=f"{index + 1}", callback_data=i['id']))

    if content['next'] is not None:
        inline_ertaklar.add(next_button)
    elif content['previous'] is not None:
        inline_ertaklar.add(pervous_button)
    await call.message.delete()
    await call.message.answer(text, reply_markup=inline_ertaklar)


@dp.callback_query_handler(state=[ru_state.ru1, ru_state.ru2])
async def content_detail(call: types.CallbackQuery, state: FSMContext):
    res = requests.get(f"{DOMAIN}content_detail/",
                       params={"id": call.data},)
    content = res.json()
    print(content)
    sanitized_content_ertak = sanitize_html(content[0]['text_for_ertak'])
    sanitized_content_sher = sanitize_html(content[0]['text_for_sher'])
    sanitized_content_oyin = sanitize_html(content[0]['text_for_oyin'])
    title = content[0]['title']

    image_path = f"/home/rasulbek/PycharmProjects/mukammal-bot-paid/erkatoy_django{content[0]['image_for_ertak']}"
    music_path = f"/home/rasulbek/PycharmProjects/mukammal-bot-paid/erkatoy_django{content[0]['music_for_sher']}"
    if content[0]['text_for_ertak']:
        sanitized_content_ertak = f"<blockquote>{title}</blockquote>  \n\n  {remove_non_breaking_spaces(sanitized_content_ertak)}"
        if len(sanitized_content_ertak) > 1024:
            left = 0
            right = 1024
            for i in range(len(sanitized_content_ertak)//1024+1):
                if left < 1024:
                    try:
                        with open(image_path, 'rb') as photo:
                            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=sanitized_content_ertak[left:right], reply_markup=back_keyboard, protect_content=True)
                    except FileNotFoundError:
                        await bot.send_message(chat_id=call.message.chat.id, text=sanitized_content_ertak[left:right], reply_markup=back_keyboard)
                else:
                    with open(image_path, 'rb') as photo:
                        await bot.send_message(chat_id=call.message.chat.id, text=f"<b>{title}(davomi)</b>\n\n{sanitized_content_ertak[left:right]}", parse_mode='HTML', reply_markup=back_keyboard, protect_content=True)
                left += 1024
                right += 1024
        else:
            try:
                with open(image_path, 'rb') as photo:
                    await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=sanitized_content_ertak[:1024], parse_mode='HTML', reply_markup=back_keyboard, protect_content=True)
            except FileNotFoundError:
                await bot.send_message(chat_id=call.message.chat.id, text=sanitized_content_ertak[:1024], reply_markup=back_keyboard)

        await uz_state.uz2.set()

    elif content[0]['text_for_sher']:
        if len(sanitized_content_sher) > 1024:
            left = 0
            right = 1024
            sanitized_content_sher = f"<blockquote>{title}</blockquote>  \n\n  {remove_non_breaking_spaces(sanitized_content_sher)}"
            for i in range(len(sanitized_content_sher)//1024+1):
                if left < 1024:
                    with open(image_path, 'rb') as photo:
                        await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=sanitized_content_sher[left:right], parse_mode='HTML', reply_markup=back_keyboard, protect_content=True)
                else:
                    with open(image_path, 'rb') as photo:
                        await bot.send_message(chat_id=call.message.chat.id, text=f"<b>{title}(davomi)</b>\n\n{sanitized_content_sher[left:right]}", parse_mode='HTML', reply_markup=back_keyboard, protect_content=True)
                left += 1024
                right += 1024
        else:
            with open(image_path, 'rb') as photo:
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=sanitized_content_sher[0:1024], parse_mode='HTML', reply_markup=back_keyboard)
        if content[0]['music_for_sher']:
            with open(music_path, 'rb') as music:
                await bot.send_audio(chat_id=call.message.chat.id, audio=music, reply_markup=back_keyboard, protect_content=True)
    elif content[0]['qoshiq']:
        qoshiq = types.InputFile(
            path_or_bytesio=f"/home/rasulbek/PycharmProjects/mukammal-bot-paid/erkatoy_django{content[0]['qoshiq']}")

        await bot.send_video(chat_id=call.message.chat.id, video=qoshiq, reply_markup=back_keyboard)
    elif content[0]['text_for_oyin']:

        if len(sanitized_content_oyin) > 1024:
            left = 0
            right = 1024
            sanitized_content_oyin = f"<blockquote>{title}</blockquote>  \n\n  {remove_non_breaking_spaces(sanitized_content_oyin)}"
            for i in range(len(sanitized_content_oyin)//1024+1):
                if left < 1024:
                    with open(image_path, 'rb') as photo:
                        await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=sanitized_content_oyin[left:right], parse_mode='HTML', reply_markup=back_keyboard, protect_content=True)
                else:
                    with open(image_path, 'rb') as photo:
                        await bot.send_message(chat_id=call.message.chat.id, text=f"<b>{title}(davomi)</b>\n\n{sanitized_content_oyin[left:right]}", parse_mode='HTML', reply_markup=back_keyboard, protect_content=True)
                left += 1024
                right += 1024
        else:
            with open(image_path, 'rb') as photo:
                await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=sanitized_content_oyin[0:1024], parse_mode='HTML', reply_markup=back_keyboard)
    elif content[0]['video_for_mohir']:
        mohir_path = f"/home/rasulbek/PycharmProjects/mukammal-bot-paid/erkatoy_django{content[0]['video_for_mohir']}"
        with open(mohir_path, 'rb') as mohir:
            await bot.send_video(chat_id=call.message.chat.id, video=mohir, reply_markup=back_keyboard)

    elif content[0]['rasm']:
        photo = types.InputFile(
            path_or_bytesio=f"/home/rasulbek/PycharmProjects/mukammal-bot-paid/erkatoy_django{content[0]['rasm']}")
        await bot.send_photo(call.message.chat.id, photo=photo)
