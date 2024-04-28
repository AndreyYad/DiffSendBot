from handlers.generic import register_generic_handlers
from handlers.callbacks import register_callbacks

async def register_handlers():
    await register_generic_handlers()
    await register_callbacks()