import datetime
import os
from sqlalchemy import (MetaData, String, Text, ForeignKey, Enum, DateTime, JSON)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
metadata = MetaData()

class Status(Enum):
    OPEN = 'открыт'
    IN_WORK = 'в работе'
    SOLVED = 'решен'
    CLOSED = 'закрыт'

class Base(DeclarativeBase):
    pass

class Clients(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_name: Mapped[str] = mapped_column(String(100))
    client_age: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class Agents(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(primary_key=True)
    agent_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    knowledge_base_content: Mapped[str] = mapped_column(Text, nullable=False)


class Tickets(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), nullable=False)
    status: Mapped[Status] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), nullable=False)

    client: Mapped["Clients"] = relationship(back_populates="clients")
    agent: Mapped["Agents"] = relationship(back_populates="agents")


class KnowledgeForTicket(Base):
    __tablename__ = "knowledge_for_ticket"

    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), primary_key=True)
    knowledge_id: Mapped[int] = mapped_column(ForeignKey("knowledge_base.id"), primary_key=True)

    ticket: Mapped["Tickets"] = relationship(back_populates="tickets")
    knowledge: Mapped["KnowledgeBase"] = relationship(back_populates="knowledge_base")

async def get_db():
    async with async_session() as session:
        yield session