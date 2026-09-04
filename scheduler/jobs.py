# scheduler/jobs.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from database.crud import get_due_reminders, mark_reminder_sent

scheduler = AsyncIOScheduler()

async def send_reminders():
    reminders = await get_due_reminders()
    for rem in reminders:
        await bot.send_message(rem.user.telegram_id, f"⏰ Напоминание:\n{rem.text}")
        await mark_reminder_sent(rem.id)

scheduler.add_job(send_reminders, 'interval', minutes=1)