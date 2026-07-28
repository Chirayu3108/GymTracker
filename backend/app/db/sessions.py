from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import Settings

settings = Settings()  # type: ignore[call-arg]

engine = create_async_engine(settings.database_url)

async_session = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False,  # Prevents unexpected I/O errors after commit
    class_=AsyncSession
  )

  