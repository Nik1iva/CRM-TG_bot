from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import UserRole

def main_menu_keyboard(role: str):
    kb = []
    kb.append([InlineKeyboardButton(text="📋 Клиенты", callback_data="menu_clients")])
    kb.append([InlineKeyboardButton(text="📦 Заказы", callback_data="menu_orders")])
    kb.append([InlineKeyboardButton(text="📌 Мои задачи", callback_data="menu_tasks")])
    kb.append([InlineKeyboardButton(text="🔍 Поиск", callback_data="menu_search")])
    # Если роль администратора – можно добавить управление сотрудниками, но пока пропустим
    return InlineKeyboardMarkup(inline_keyboard=kb)

def clients_keyboard():
    kb = [
        [InlineKeyboardButton(text="➕ Добавить клиента", callback_data="add_client")],
        [InlineKeyboardButton(text="🔍 Найти клиента", callback_data="search_client")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def orders_keyboard():
    kb = [
        [InlineKeyboardButton(text="➕ Создать заказ", callback_data="add_order")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def tasks_keyboard():
    kb = [
        [InlineKeyboardButton(text="🔄 Мои задачи", callback_data="my_tasks")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)