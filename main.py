import asyncio
import logging
import re
import json


from random import choice
from decouple import config


from aiogram import Bot, Dispatcher, Router, types,F
from aiogram.utils import keyboard
from aiogram.filters import CommandStart, Command   
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = config("TOKEN")

dp = Dispatcher() # объект диспетчера (оброботчик событий)
bot = Bot(TOKEN)

# async - асинхронная функция (позволяет не блокировать выполнение кода)
# await - ожидание выполнения асинхронной функции


#MENU
mainmenu = keyboard.InlineKeyboardBuilder()
mainmenu.row(types.InlineKeyboardButton(text="🎮Випадкова Гра", callback_data="random_game"))

all_games_data = []
with open("metacritic.json", "r", encoding="utf-8") as file:
    all_games_data = json.load(file)
    

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привіт! Я бот для пошуку ігор на Metacritic",reply_markup=mainmenu.as_markup())



@dp.callback_query(F.data == "random_game")
async def random_game(call: types.CallbackQuery, state: FSMContext):
    game = choice(all_games_data)
    text = f"<b>{game['title']}</b>\n\n{game['description']}\n\n<i>MetaScore:</i> {game['meta_score']}"
    await call.message.answer_photo(photo=game["img"], caption=text, reply_markup=mainmenu.as_markup(), parse_mode="HTML")
    await call.message.delete()

    



async def main() -> None:
    await bot.set_my_commands([], scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())