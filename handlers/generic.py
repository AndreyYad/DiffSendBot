from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from modules.bot_commands import send_msg, forward_msg
from modules.text import Text
from modules.config import CHAT_ID, BOT_ID
from modules.markups import markup_set_recipient, markup_cancel_state
from modules.database import save_message, get_user_id

router = Router()

async def start_func(msg: Message):
    await send_msg(
        msg.chat.id, 
        Text.start
    )

    # from pprint import PrettyPrinter
    # pp = PrettyPrinter(indent=4)
    # pp.pprint(msg.reply_to_message.poll.__dict__)

async def set_recipient_func(msg: Message):
    await send_msg(
        msg.chat.id,
        Text.what_set_rec,
        await markup_set_recipient()
    )

async def see_recipient_func(msg: Message, state: FSMContext):
    # print(await state.get_data())
    data = await state.get_data()
    if data:
        await send_msg(
            msg.chat.id,
            Text.see_rec.format(data['name']),
            await markup_cancel_state()
        )
    else:
        await send_msg(
            msg.chat.id,
            Text.not_selected_rec
        )

async def send_msg_func(msg: Message, state: FSMContext):

    if await state.get_state() is None:
        await send_msg(
            msg.chat.id,
            Text.not_selected_rec
        )
    else:
        data = await state.get_data()
        await send_msg(
            CHAT_ID,
            data['tag']
        )
        frw_msg = await forward_msg(
            CHAT_ID,
            msg.from_user.id,
            msg.message_id
        )
        await save_message(frw_msg.message_id, msg.from_user.id)
        await send_msg(
            msg.from_user.id,
            Text.send_succes_rec.format(data['name'])
        )

async def reply_to_msg_func(msg: Message):
    text = msg.text[6:]

    user_id = await get_user_id(msg.reply_to_message.message_id)
    if user_id == 0:
        user_id = msg.reply_to_message.forward_from.id

    await send_msg(
        user_id,
        text
    )
    await send_msg(
        msg.chat.id,
        Text.send_succes
    )

async def register_generic_handlers():
    router.message.register(lambda msg: print(msg.chat.id), Command('id'))
    router.message.register(start_func, CommandStart(), F.chat.type == 'private')
    router.message.register(set_recipient_func, Command('set_recipient'), F.chat.type == 'private')
    router.message.register(see_recipient_func, Command('see_recipient'), F.chat.type == 'private')
    router.message.register(send_msg_func, F.chat.type == 'private')
    router.message.register(
        reply_to_msg_func, 
        F.chat.id == CHAT_ID,
        F.reply_to_message.from_user.id == BOT_ID,
        F.text.func(lambda text: text.startswith('!send '))
    )