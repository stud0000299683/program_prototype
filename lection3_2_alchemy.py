import asyncio
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(128), index=True)
    password = Column(String(128), index=True)

    role = Column(Integer, ForeignKey(
        "roles.id",
        ondelete="CASCADE"
    )
    )

    roles = relationship("Roles", back_populates="users", lazy="subquery")

    def __repr__(self):
        return f"{self.id}-{self.login}-{self.password}-{self.role}"


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), index=True)
    level = Column(Integer, unique=True, index=True)

    users = relationship("User", back_populates="roles", lazy="subquery")

    def __repr__(self):
        return f"{self.id}-{self.name}-{self.level}"

async  def create_db():
    # docker run -- pg_test -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:latest
    PG_URL = 'postgresql+asyncpg://postgres:postgre@localhost:5433/postgres'

    engine = create_async_engine(PG_URL)
    async  with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

if __name__ in "__main__":
    asyncio.run(create_db())
