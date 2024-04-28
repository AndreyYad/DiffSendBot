from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from modules.bot_commands import edit_msg_text
from modules.states import FSMClient
from modules.text import Text
from modules.config import RECIPIENTS, CHAT_ID

router = Router()

async def callback_set_state(call: CallbackQuery, state: FSMContext):
    await state.set_state(FSMClient.recipient_selected)
    await state.set_data(RECIPIENTS[int(call.data[6:])])
    await edit_msg_text(
        Text.set_rec.format((await state.get_data())['name']),
        call.message.chat.id,
        call.message.message_id
    )

async def callback_cancel_state(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await edit_msg_text(
        Text.cancel_rec,
        call.message.chat.id,
        call.message.message_id
    )
                
async def register_callbacks():
    router.callback_query.register(callback_set_state, F.data.startswith('state_'))
    router.callback_query.register(callback_cancel_state, F.data == 'cancel_state')