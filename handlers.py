from aiogram.filters import Command
from aiogram import types, Router, Bot
import datetime
from weather import get_weather_next_day
from aiogram.types import InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from state import GuestName
from utils import dict_to_string
from redisdb import start_sesion, zero_variables
import json
from buttons import buttons_start, keyboard
from config import TOKEN
from redisdb import get_variables

TOKEN = TOKEN
bot = Bot(TOKEN)
router = Router()
r = start_sesion()
event_players_dict = get_variables().get("event_players_dict")


async def send_message():
    r.hset('VolleyBot', 'event_players_dict', json.dumps(dict()))
    if get_variables().get("message"):
        await get_variables().get("message").unpin()
    message = await bot.send_message(text=get_weather_next_day(),
                                     chat_id=get_variables().get("chat_id"),
                                     message_thread_id=get_variables().get("topik_id"),
                                     reply_markup=keyboard)
    r.hset('VolleyBot', 'message_id', json.dumps(message.message_id))
    await message.pin()


async def edit_message():
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_start)
    await bot.edit_message_text(text=get_weather_next_day() +
                                     dict_to_string(event_players_dict) +
                                     '\nUpdated ' +
                                     datetime.datetime.now().strftime("%H:%M:%S"),
                                chat_id=get_variables().get("chat_id"),
                                reply_markup=keyboard,
                                message_id=get_variables().get("message_id")
                                )


@router.message(Command('start'))
async def start(message: types.Message):
    zero_variables()
    await message.answer('Bot activate')

    r.hset('VolleyBot', 'chat_id', json.dumps(message.chat.id))
    r.hset('VolleyBot', 'topik_id', json.dumps(message.message_thread_id))
    r.hset('VolleyBot', 'admin_id', json.dumps(message.from_user.id))
    await send_message()


@router.callback_query(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    pushed_user_id = str(callback_query.from_user.id)
    pushed_name = callback_query.from_user.full_name
    current_time = int(datetime.datetime.now().timestamp())

    if callback_query.data == 'go':
        if pushed_user_id not in event_players_dict.keys():
            event_players_dict[pushed_user_id] = {pushed_name: current_time}
        else:
            if pushed_name not in event_players_dict[pushed_user_id].keys():
                event_players_dict[pushed_user_id][pushed_name] = current_time
            else:
                await callback_query.answer(f'You are already on the list', show_alert=True)
    elif callback_query.data == 'dont':
        if pushed_user_id in event_players_dict.keys() and pushed_name in event_players_dict[pushed_user_id]:
            event_players_dict[pushed_user_id].pop(pushed_name)
            await callback_query.answer(f'Player removed', show_alert=True)

    elif callback_query.data == 'add':
        if (callback_query.from_user.id != int(get_variables().get("admin_id"))
                and (event_players_dict.get(pushed_user_id)
                     and len(event_players_dict[pushed_user_id]) > 1)
                or (event_players_dict.get(pushed_user_id)
                    and len(event_players_dict[pushed_user_id]) == 1
                    and pushed_name not in event_players_dict[pushed_user_id].keys())):
            await callback_query.answer(f'{callback_query.from_user.full_name}, you have already added a player!',
                                        show_alert=True)
        else:
            await callback_query.answer(f"{callback_query.from_user.full_name}, please enter the player's name:", show_alert=True)
            if pushed_user_id not in event_players_dict.keys():
                event_players_dict[pushed_user_id] = dict()
                await state.set_state(GuestName.Name)

            else:
                await state.set_state(GuestName.Name)

    elif callback_query.data == 'del':
        if pushed_user_id in event_players_dict.keys():

            name = callback_query.from_user.full_name
            for player in event_players_dict[pushed_user_id].keys():
                if player != name:
                    event_players_dict[pushed_user_id].pop(player)
                    await callback_query.answer(f'Player {player} has been removed', show_alert=True)
                    break
            else:
                await callback_query.answer(f"You haven't added a player yet!", show_alert=True)
    r.hset('VolleyBot', 'event_players_dict', json.dumps(event_players_dict))
    await edit_message()
    r.close()


@router.message(GuestName.Name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text.strip().capitalize()
    current_time = int(datetime.datetime.now().timestamp())
    event_players_dict[str(message.from_user.id)][name] = current_time
    await bot.delete_messages(chat_id=get_variables().get("chat_id"),
                              message_ids=[message.message_id])
    await state.update_data(Name=name)
    await state.clear()
    await edit_message()
    r.hset('VolleyBot', 'event_players_dict', json.dumps(event_players_dict))
    r.close()


@router.message(GuestName.del_Name)
async def del_name(message: types.Message, state: FSMContext):
    name = message.text.strip().capitalize()
    if name in event_players_dict[message.from_user.id].keys():
        event_players_dict[message.from_user.id].pop(name)
        await bot.delete_messages(chat_id=get_variables().get("chat_id"),
                                  message_ids=[message.message_id])
    else:
        await message.answer(text=f"You haven't added a player with the name {name}!")

        await bot.delete_messages(chat_id=get_variables().get("chat_id"),
                                  message_ids=[message.message_id])
    await state.update_data(Name=name)
    await state.clear()
    await edit_message()
    r.close()


@router.message()
async def wrong_topik(message: types.Message):
    if message.message_thread_id == get_variables().get("topik_id"):
        await message.delete()
