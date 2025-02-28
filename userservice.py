from lection3_2_alchemy import User, Roles

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


async  def add_role(name, level):
    PG_URL = 'postgresql+asyncpg://postgres:postgre@localhost:5433/postgres'
    engine = create_async_engine(PG_URL)
    session = sessionmaker(
        engine,
        class_ = AsyncSession,
        expire_on_commit=False)
    role = Roles(name=name, level=level)

    async  with session() as db:
        db.add(role)
        await db.commit()

        return role

class RoleService():
    def __init__(self, db_url):
        self.db_url = db_url

    def get_async_session(self) -> AsyncSession:
        engine = create_async_engine(self.db_url)

        return sessionmaker(engine,
                            class_=AsyncSession,
        expire_on_commit=False
        )

    async def add_role(self, name, level):
        session = self.get_async_session()
        role = Roles(name=name, level=level)

        async  with session() as db:
            db.add(role)
            await db.commit()
            return role

async  def runner():
    PG_URL = 'postgresql+asyncpg://postgres:postgre@localhost:5433/postgres'
    role_service = RoleService(PG_URL)

    res = await add_role(name="superuser", level=6)
    print(res)
if __name__ == "__main__":
    asyncio.run(runner())
