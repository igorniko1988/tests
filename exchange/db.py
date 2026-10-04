import enum
import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from exchange.config import settings

engine = create_async_engine(settings.database_url, pool_size=10, max_overflow=20)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

AMOUNT = Numeric(36, 18)


def utcnow() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class OrderSide(enum.StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(enum.StrEnum):
    LIMIT = "LIMIT"


class OrderStatus(enum.StrEnum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Balance(Base):
    __tablename__ = "balances"
    __table_args__ = (UniqueConstraint("user_id", "asset"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    asset: Mapped[str] = mapped_column(String(10))
    available: Mapped[Decimal] = mapped_column(AMOUNT, default=Decimal(0))
    locked: Mapped[Decimal] = mapped_column(AMOUNT, default=Decimal(0))


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    symbol: Mapped[str] = mapped_column(String(20))
    side: Mapped[OrderSide] = mapped_column(Enum(OrderSide, native_enum=False))
    type: Mapped[OrderType] = mapped_column(Enum(OrderType, native_enum=False))
    price: Mapped[Decimal] = mapped_column(AMOUNT)
    quantity: Mapped[Decimal] = mapped_column(AMOUNT)
    filled_quantity: Mapped[Decimal] = mapped_column(AMOUNT, default=Decimal(0))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, native_enum=False), default=OrderStatus.NEW
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class IdempotencyKey(Base):
    """Сохранённый ответ на запрос с заголовком Idempotency-Key."""

    __tablename__ = "idempotency_keys"
    __table_args__ = (UniqueConstraint("user_id", "key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    key: Mapped[str] = mapped_column(String(255))
    request_hash: Mapped[str] = mapped_column(String(64))
    status_code: Mapped[int]
    response_body: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


async def get_session():
    async with SessionLocal() as session:
        yield session


async def create_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


__all__ = [
    "AsyncSession",
    "Balance",
    "IdempotencyKey",
    "Order",
    "OrderSide",
    "OrderStatus",
    "OrderType",
    "User",
]
