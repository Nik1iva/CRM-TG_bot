from sqlalchemy import select
from database.engine import async_session_maker
from database.models import User

async def get_user_by_telegram_id(telegram_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

# Позже сюда добавятся функции get_due_reminders, mark_reminder_sent и другие
async def get_due_reminders():
    # Временно возвращаем пустой список
    return []

async def mark_reminder_sent(reminder_id):
    # Заглушка
    pass