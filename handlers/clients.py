from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from database.engine import async_session_maker
from database.models import Client
from keyboards.inline import clients_keyboard
import re

router = Router()

class AddClient(StatesGroup):
    name = State()
    phone = State()
    email = State()
    comment = State()

@router.callback_query(F.data == "add_client")
async def add_client_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Введите имя клиента:")
    await state.set_state(AddClient.name)

@router.message(AddClient.name)
async def add_client_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите телефон клиента (в формате +7XXXXXXXXXX):")
    await state.set_state(AddClient.phone)

@router.message(AddClient.phone)
async def add_client_phone(message: types.Message, state: FSMContext):
    phone = re.sub(r'\D', '', message.text)
    if len(phone) < 10:
        await message.answer("Слишком короткий номер. Попробуйте ещё раз:")
        return
    await state.update_data(phone=phone)
    await message.answer("Введите email (или '-' если нет):")
    await state.set_state(AddClient.email)

@router.message(AddClient.email)
async def add_client_email(message: types.Message, state: FSMContext):
    email = message.text if message.text != '-' else None
    await state.update_data(email=email)
    await message.answer("Введите комментарий (или '-' если нет):")
    await state.set_state(AddClient.comment)

@router.message(AddClient.comment)
async def add_client_comment(message: types.Message, state: FSMContext):
    comment = message.text if message.text != '-' else None
    data = await state.get_data()
    async with async_session_maker() as session:
        new_client = Client(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email'),
            comment=comment
        )
        session.add(new_client)
        await session.commit()
    await message.answer(f"✅ Клиент {data['name']} добавлен!")
    await state.clear()
    await message.answer("Что дальше?", reply_markup=clients_keyboard())