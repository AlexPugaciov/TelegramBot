
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


buttons_start = [
    [InlineKeyboardButton(text="✅I'm going", callback_data='go'),
     InlineKeyboardButton(text='❌Not going', callback_data='dont')],
    [InlineKeyboardButton(text='✅Add player', callback_data='add'),
     InlineKeyboardButton(text='❌Remove player', callback_data='del')],
    [InlineKeyboardButton(text='Update weather', callback_data='update')]]
keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_start)
