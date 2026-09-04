from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.engine import async_session_maker
from database.models import User, UserRole
from database.crud import get_user_by_telegram_id
from keyboards.inline import main_menu_keyboard   # синхронная функция
import re
import os
from dotenv import load_dotenv

router = Router()
load_dotenv()

# (Опционально) Список администраторов из .env
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

# FSM состояния для регистрации
class Registration(StatesGroup):
    full_name = State()
    phone = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if user:
        # Показываем главное меню, передаём роль
        await message.answer(
            f"С возвращением, {user.full_name}!",
            reply_markup=main_menu_keyboard(user.role)   # <-- синхронная, без await
        )
    else:
        await message.answer("Добро пожаловать! Для начала работы давайте зарегистрируемся.\nВведите ваше полное имя:")
        await state.set_state(Registration.full_name)

@router.message(Registration.full_name)
async def reg_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Теперь введите ваш номер телефона (в формате +7XXXXXXXXXX):")
    await state.set_state(Registration.phone)

@router.message(Registration.phone)
async def reg_phone(message: types.Message, state: FSMContext):
    phone = re.sub(r'\D', '', message.text)  # оставляем только цифры
    if len(phone) < 10:
        await message.answer("Номер слишком короткий. Введите в формате +7XXXXXXXXXX")
        return
    
    data = await state.get_data()
    
    # Определяем роль – если пользователь в списке админов, даём ADMIN, иначе EMPLOYEE
    role = UserRole.ADMIN if message.from_user.id in ADMIN_IDS else UserRole.EMPLOYEE
    
    async with async_session_maker() as session:
        new_user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=data['full_name'],
            phone=phone,
            role=role
        )
        session.add(new_user)
        await session.commit()
    
    await message.answer("✅ Регистрация завершена! Теперь вы можете пользоваться ботом.")
    await state.clear()
    
    # Получаем созданного пользователя и показываем меню
    user = await get_user_by_telegram_id(message.from_user.id)
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_keyboard(user.role)   # синхронная, без await
    )