import asyncio
import asyncpg
from app.core.database import engine, Base, DATABASE_URL
from app.models.user import User
from app.models.shared_track import SharedTrack
from app.models.reactions import Reaction
from app.models.track import Track
from app.models.friendship import Friendship
from app.models.friendship_status import FriendshipStatus
from app.models.music_platform import MusicPlatform


async def test_connect():
    asyncpg_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(asyncpg_url)
    print("Подключение через asyncpg успешно!")
    await conn.close()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Все таблицы созданы!")


async def main():
    await test_connect()
    await init_models()


if __name__ == "__main__":
    asyncio.run(main())
