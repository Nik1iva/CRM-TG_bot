from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database.models import Base
from config import DATABASE_URL

# Создаем движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий для работы с БД
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Функция создания таблиц (запускается при старте)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)