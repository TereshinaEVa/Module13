from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(text=['Calories'])
async def set_age(massage):
    await massage.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(massage, state):
    await state.update_data(age=int(massage.text))
    #data = await state.get_data()
    await massage.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(massage, state):
    await state.update_data(growth=int(massage.text))
    #data = await state.get_data()
    await massage.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(massage, state):
    await state.update_data(weight=int(massage.text))
    data = await state.get_data()
    kall = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] - 161
    await massage.answer(f'Норма каллорий: {kall}')
    await  state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)