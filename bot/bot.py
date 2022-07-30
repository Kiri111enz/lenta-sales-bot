from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import bot._config as cfg

_bot = Bot(token=cfg.BOT_TOKEN)
_dp = Dispatcher(_bot, storage=MemoryStorage())


class _States(StatesGroup):
    town = State()
    shop = State()
    category = State()
    sub_category = State()
    item = State()


def start() -> None:
    executor.start_polling(_dp)


@_dp.message_handler(state='*', commands='начать')
async def _start(message: types.Message) -> None:
    await _States.town.set()
    await message.answer('Добро пожаловать! В этом боте ты сможешь узнавать о скидках в Ленте.\n'
                         'Для начала нужно выбрать интересующий город.\n'
                         'Позже ты сможешь изменить свой выбор.')


@_dp.message_handler(state='*', commands='город')
@_dp.message_handler(state=_States.town)
async def _town(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['town'] = message.text

    await _States.shop.set()
    await message.answer('Город выбран. Теперь выбери магазин.')


@_dp.message_handler(state='*', commands='магазин')
@_dp.message_handler(state=_States.shop)
async def _shop(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['shop'] = message.text

    await _States.category.set()
    await message.answer('Магазин выбран. Теперь выбери категорию товаров.')


@_dp.message_handler(state='*', commands='категория')
@_dp.message_handler(state=_States.category)
async def _category(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['category'] = message.text

    await _States.sub_category.set()
    await message.answer('Категория выбрана. Теперь выбери подкатегорию товаров.')


@_dp.message_handler(state='*', commands='подкатегория')
@_dp.message_handler(state=_States.sub_category)
async def _sub_category(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['sub_category'] = message.text

    await _States.item.set()
    await message.answer('Вот список товаров со скидкой. Чтобы увидеть подробную информацию, введи номер товара.')


@_dp.message_handler(state='*', commands='товар')
@_dp.message_handler(state=_States.item)
async def _item(message: types.Message) -> None:
    await message.answer('Подробная информация о товаре.')
