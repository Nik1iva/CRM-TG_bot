from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, or_
from database.engine import async_session_maker
from database.models import Client
from keyboards.inline import clients_keyboard

router = Router()

class SearchClients(StatesGroup):
    query = State()

@router.callback_query(F.data == "search_client")
async def search_client_prompt(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Введите имя или телефон для поиска:")
    await state.set_state(SearchClients.query)

@router.message(SearchClients.query)
async def search_client_execute(message: types.Message, state: FSMContext):
    query = message.text.strip()
    async with async_session_maker() as session:
        stmt = select(Client).where(
            or_(
                Client.name.ilike(f"%{query}%"),
                Client.phone.ilike(f"%{query}%")
            )
        )
        result = await session.execute(stmt)
        clients = result.scalars().all()
    
    if not clients:
        await message.answer("Ничего не найдено.")
    else:
        text = "🔍 Результаты поиска:\n"
        for c in clients:
            text += f"👤 {c.name} | 📞 {c.phone}"
            if c.email:
                text += f" | ✉️ {c.email}"
            text += "\n"
        await message.answer(text)
    
    await state.clear()
    # Возвращаемся в меню клиентов
    await message.answer("Поиск завершён.", reply_markup=clients_keyboard())