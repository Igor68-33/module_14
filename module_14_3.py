# Доработка бота
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from config import TOKEN
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

in_kb = types.InlineKeyboardMarkup()
in_button1 = types.InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = types.InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_kb.add(in_button1)
in_kb.insert(in_button2)

# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
# У всех кнопок назначьте callback_data="product_buying"
in_kb2 = types.InlineKeyboardMarkup()
in_kb2_button1 = types.InlineKeyboardButton(text='Product1', callback_data='product_buying')
in_kb2_button2 = types.InlineKeyboardButton(text='Product2', callback_data='product_buying')
in_kb2_button3 = types.InlineKeyboardButton(text='Product3', callback_data='product_buying')
in_kb2_button4 = types.InlineKeyboardButton(text='Product4', callback_data='product_buying')
in_kb2.add(in_kb2_button1)
in_kb2.insert(in_kb2_button2)
in_kb2.add(in_kb2_button3)
in_kb2.insert(in_kb2_button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_(message):
    await message.answer('Привет, я бот помогающий вашему здоровью.\nВыберите действие.',
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="Рассчитать"),
                                     KeyboardButton(text="Информация"),
                                 ],
                                 [KeyboardButton(text='Купить')],
                             ],
                             resize_keyboard=True, one_time_keyboard=True),
                         )


# Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
@dp.message_handler(text='Купить')
async def get_buying_list(message):
    # Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза.
    # После каждой надписи выводите картинки к продуктам.
    # В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".
    for i in range(1, 5):
        await message.answer(f"Product{i} | Описание: описание {i} | Цена: {i * 100}")
        await bot.send_photo(message.from_user.id, photo=open(f'BAD_{i}.webp', 'rb'))
    await message.answer(f"Выберите продукт для покупки:", reply_markup=in_kb2)


# Callback хэндлер, который реагирует на текст "product_buying"
@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(callback_query: types.CallbackQuery):
    # Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"
    await callback_query.message.answer("Вы успешно приобрели продукт!")
    await callback_query.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu_1(message):
    await message.answer(text='Выберите опцию:', reply_markup=in_kb)


@dp.message_handler(text='Информация')
async def main_menu_2(message):
    await message.answer(text='Я бот, который умеет проводить расчёты.')


@dp.callback_query_handler(text='calories')
async def some_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Введите свой возраст (полных лет)')
    await callback_query.answer()
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def get_formulas(callback_query: types.CallbackQuery):
    formulas_text = ("1. Упрощенный вариант формулы Миффлина-Сан Жеора - \n"
                     "необходимое количество килокалорий (ккал) в сутки для каждого конкретного человека:\n"
                     "   для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;)\n"
                     "   для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.")
    await callback_query.message.answer(formulas_text)
    # сайт с формулами
    # await callback_query.message.answer('https://www.calc.ru/Formula-Mifflinasan-Zheora.html')
    await callback_query.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # проверим правильность ввода данных и корректность результата
    try:
        Calories_man = float(data["weight"]) * 10 + 6.25 * float(data["growth"]) - 5 * float(data["age"]) + 5
        Calories_wuman = float(data["weight"]) * 10 + 6.25 * float(data["growth"]) - 5 * float(data["age"]) - 161
        if Calories_wuman < 0:
            raise ValueError
        await message.answer(f'Норма калорий в сутки:\n'
                             f'   для мужчин: {Calories_man}\n'
                             f'   для женщин: {Calories_wuman}')
    except:
        await message.answer(f'Данные были введены неверно, повторите расчёт снова:')
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
