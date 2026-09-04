from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from keyboards.inline import (
    main_menu_keyboard,
    clients_keyboard,
    orders_keyboard,
    tasks_keyboard
)
from database.crud import get_user_by_telegram_id

router = Router()


# Обработчики кнопок главного меню
@router.callback_query(F.data == "menu_clients")
async def menu_clients(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📋 Раздел клиентов.\nИспользуйте кнопки ниже:",
        reply_markup=clients_keyboard()
    )

@router.callback_query(F.data == "menu_orders")
async def menu_orders(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📦 Раздел заказов.",
        reply_markup=orders_keyboard()
    )

@router.callback_query(F.data == "menu_tasks")
async def menu_tasks(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📌 Ваши задачи.",
        reply_markup=tasks_keyboard()
    )

@router.callback_query(F.data == "menu_search")
async def menu_search(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🔍 Введите поисковый запрос (имя, телефон или часть):"
    )
    # Здесь вы позже добавите переход в состояние SearchClients.query

# Обработчик кнопки "Назад" – возвращает в главное меню
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.answer()
    # Если пользователь зарегистрирован, показываем меню с его ролью
    user = await get_user_by_telegram_id(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            "Главное меню:",
            reply_markup=main_menu_keyboard(user.role)
        )
    else:
        # Если не зарегистрирован – отправляем на старт
        await callback.message.edit_text("Пожалуйста, зарегистрируйтесь через /start")