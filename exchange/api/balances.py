import uuid
from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from exchange.api.deps import Session, UserId
from exchange.db import Balance
from exchange.schemas import ASSETS, BalanceOut, DepositRequest

router = APIRouter(tags=["balances"])


async def lock_balance(session: AsyncSession, user_id: uuid.UUID, asset: str) -> Balance:
    """Берёт строку баланса под SELECT ... FOR UPDATE, создавая её при необходимости."""
    await session.execute(
        insert(Balance)
        .values(user_id=user_id, asset=asset, available=Decimal(0), locked=Decimal(0))
        .on_conflict_do_nothing(index_elements=["user_id", "asset"])
    )
    return await session.scalar(
        select(Balance).where(Balance.user_id == user_id, Balance.asset == asset).with_for_update()
    )


@router.get("/balances", response_model=list[BalanceOut])
async def list_balances(user_id: UserId, session: Session):
    rows = await session.scalars(select(Balance).where(Balance.user_id == user_id))
    by_asset = {b.asset: b for b in rows}
    return [
        by_asset.get(asset) or BalanceOut(asset=asset, available=Decimal(0), locked=Decimal(0))
        for asset in ASSETS
    ]


@router.post("/balances/deposit", response_model=BalanceOut)
async def deposit(body: DepositRequest, user_id: UserId, session: Session):
    balance = await lock_balance(session, user_id, body.asset)
    balance.available += body.amount
    await session.commit()
    return balance
