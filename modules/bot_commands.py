'''
Модуль с командами для бота
'''

from loguru import logger
from aiogram import types
from aiogram import exceptions

from bot.bot import bot

empty_markups = types.InlineKeyboardMarkup(inline_keyboard=[[]])

async def send_msg(chat_id: int, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Отправка сообщения'''
    return await bot.send_message(chat_id, text, reply_markup=markup, **kwargs)

async def send_msg_photo(chat_id: int, photo: types.InputFile, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Отправка фото'''
    return await bot.send_photo(chat_id, photo, caption=text, reply_markup=markup, **kwargs)

async def reply_msg(msg: types.Message, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Ответ на сообщение'''
    return await msg.reply(text, reply_markup=markup, **kwargs)
    
async def edit_msg_text(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Редактирование сообщения'''
    try:
        await bot.edit_message_text(text, chat_id, msg_id, reply_markup=markup, **kwargs)
        return True
    except exceptions.TelegramBadRequest as error:
        logger.error(error)
        return False
        
async def delete_msg(chat_id: int, msg_id: int):
    '''Удаление сообщения'''
    await bot.delete_message(chat_id, msg_id)

async def forward_msg(chat_id_to: int, chat_id_from: int, msg_id: int, anonim: bool=False, **kwargs):
    '''Пересылка сообщения'''
    if not anonim:
        return await bot.forward_message(chat_id_to, chat_id_from, msg_id, **kwargs)
    else:
        return await bot.copy_message(chat_id_to, chat_id_from, msg_id, **kwargs)

if __name__ == '__main__':
    # run()
    pass