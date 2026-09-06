from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select
from database.engine import async_session_maker
from database.models import Order, Client
from keyboards.inline import orders_keyboard
import re

router = Router()

class AddOrder(StatesGroup):
    client_phone = State()
    service = State()
    amount = State()

@router.callback_query(F.data == "add_order")
async def add_order_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Введите телефон клиента для заказа (в формате +7XXXXXXXXXX):")
    await state.set_state(AddOrder.client_phone)

@router.message(AddOrder.client_phone)
async def add_order_phone(message: types.Message, state: FSMContext):
    phone = re.sub(r'\D', '', message.text)  # оставляем только цифры
    async with async_session_maker() as session:
        stmt = select(Client).where(Client.phone == phone)
        result = await session.execute(stmt)
        client = result.scalar_one_or_none()
    if not client:
        await message.answer("❌ Клиент с таким телефоном не найден. Сначала добавьте клиента через раздел 'Клиенты'.")
        await state.clear()
        return
    await state.update_data(client_id=client.id)
    await message.answer(f"Клиент найден: {client.name}. Теперь введите название услуги:")
    await state.set_state(AddOrder.service)

@router.message(AddOrder.service)
async def add_order_service(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer("Введите сумму заказа (цифрами, например 1500.50):")
    await state.set_state(AddOrder.amount)

@router.message(AddOrder.amount)
async def add_order_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer("❌ Введите корректное число (например 1500.50):")
        return
    data = await state.get_data()
    async with async_session_maker() as session:
        new_order = Order(
            client_id=data['client_id'],
            service=data['service'],
            amount=amount,
            status='new'
        )
        session.add(new_order)
        await session.commit()
    await message.answer(f"✅ Заказ на услугу '{data['service']}' на сумму {amount} руб. создан!")
    await state.clear()
    await message.answer("Что дальше?", reply_markup=orders_keyboard())

@router.callback_query(F.data == "list_orders")
async def list_orders(callback: types.CallbackQuery):
    await callback.answer()
    async with async_session_maker() as session:
        stmt = select(Order).join(Client).order_by(Order.created_at.desc())
        result = await session.execute(stmt)
        orders = result.scalars().all()
    
    if not orders:
        await callback.message.edit_text("📭 Заказов пока нет.")
        return
    
    text = "📋 **Список всех заказов:**\n\n"
    for idx, order in enumerate(orders, 1):
        client_name = order.client.name if order.client else "Неизвестный клиент"
        status_emoji = {
            "new": "🆕",
            "in_progress": "🔄",
            "completed": "✅",
            "cancelled": "❌"
        }.get(order.status, "❓")
        text += (
            f"{idx}. {status_emoji} **Заказ #{order.id}**\n"
            f"   👤 {client_name}\n"
            f"   📦 {order.service}\n"
            f"   💰 {order.amount:.2f} руб.\n"
            f"   📅 {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"   ⏳ Статус: {order.status}\n\n"
        )
    
    if len(text) > 4096:
        text = text[:4000] + "\n... (слишком много заказов, показаны не все)"
    
    await callback.message.edit_text(text, parse_mode="Markdown")