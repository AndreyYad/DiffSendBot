from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .config import RECIPIENTS

async def markup_set_recipient():
    builder = InlineKeyboardBuilder()

    list_buttons = [
        InlineKeyboardButton(
            text=RECIPIENTS[index]['name'], 
            callback_data=f'state_{index}'
        ) 
        for index in range(len(RECIPIENTS))
    ]

    list_buttons.append(InlineKeyboardButton(text='Сброс', callback_data='cancel_state'))

    if len(list_buttons) <= 3:
        for button in list_buttons:
            builder.row(button)
    else:
        tuple_buttons_row = []
        for button in list_buttons:
            tuple_buttons_row.append(button)
            if len(tuple_buttons_row) == 2:
                builder.row(*tuple_buttons_row)
                tuple_buttons_row = []
        builder.row(*tuple_buttons_row)

    return builder.as_markup()

async def markup_cancel_state():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text='Сбросить', callback_data='cancel_state'))

    return builder.as_markup()