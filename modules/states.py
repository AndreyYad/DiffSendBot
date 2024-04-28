from aiogram.fsm.state import StatesGroup, State

from modules.config import RECIPIENTS

class FSMClient(StatesGroup):
    recipient_selected = State()