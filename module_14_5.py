from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import crud_functions

product = crud_functions.get_all_products()

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb_reply = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
bt_calc = KeyboardButton(text = 'Рассчитать')
bt_info = KeyboardButton(text = 'Информация')
bt_reg = KeyboardButton(text = 'Регистрация')
bt_buy = KeyboardButton(text = 'Купить')
kb_reply.add(bt_calc, bt_info, bt_reg, bt_buy)

kb_inline = InlineKeyboardMarkup()
bt_in_calc = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
bt_in_formula = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
kb_inline.row(bt_in_calc, bt_in_formula)

kb_product = InlineKeyboardMarkup(resize_keyboard = True)
bt_product1 = InlineKeyboardButton(text = 'Продукт1', callback_data = 'product_buying')
bt_product2 = InlineKeyboardButton(text = 'Продукт2', callback_data = 'product_buying')
bt_product3 = InlineKeyboardButton(text = 'Продукт3', callback_data = 'product_buying')
bt_product4 = InlineKeyboardButton(text = 'Продукт4', callback_data = 'product_buying')
kb_product.row(bt_product1, bt_product2, bt_product3, bt_product4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb_reply)

@dp.message_handler(text = 'Информация')
async def info(message):
    await message.answer('Привет! Я бот рассчитывающий количество калорий по формуле Миффлина-Сан Жеора.')

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kb_inline)

@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    for i in product:
        await message.answer(f'Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}')
        with open(f'images1/{i[0]}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup = kb_product)

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6.25 х рост (см) - 5 * возраст (лет) + 5')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 4.92 * int(data['age']) + 5
    await message.answer(f'Количество калорий: {round(calories, 2)}')
    await state.finish()

@dp.message_handler(text = 'Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state = RegistrationState.username)
async def set_username(message, state):
    if crud_functions.is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
        return
    await state.update_data(username = message.text)
    await message.answer('Введите свой email:')
    await RegistrationState.email.set()

@dp.message_handler(state = RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email = message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state = RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age = message.text)
    date = await state.get_data()
    crud_functions.add_user(date['username'], date['email'], date['age'])
    await message.answer(f'Регистрация пользователя {date["username"]} прошла успешно')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)