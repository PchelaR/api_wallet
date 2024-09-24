from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas import WalletOperation, TypeOperation
from models import WalletModel
from database import get_session


async def create_wallet(db: AsyncSession = Depends(get_session)):
    new_wallet = WalletModel()

    db.add(new_wallet)
    await db.commit()

    return new_wallet


async def get_wallet_balance(wallet_uuid: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(WalletModel).filter(WalletModel.uuid == wallet_uuid)
    )
    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise HTTPException(status_code=404, detail="Кошелёк не найден")

    return wallet


async def update_wallet(wallet_uuid: str, operation: WalletOperation, db: AsyncSession = Depends(get_session)):
    async with db.begin():
        result = await db.execute(
            select(WalletModel).filter(WalletModel.uuid == wallet_uuid).with_for_update()
        )

        wallet = result.scalar_one_or_none()

        if wallet is None:
            raise HTTPException(status_code=404, detail="Кошелёк не найден")

        if operation.operation == TypeOperation.DEPOSIT:
            wallet.balance += operation.amount
        elif operation.operation == TypeOperation.WITHDRAW:
            if wallet.balance < operation.amount:
                raise HTTPException(status_code=400, detail="Недостаточно средств")
            wallet.balance -= operation.amount
        else:
            raise HTTPException(status_code=400, detail="Неизвестная операция")

    await db.commit()

    return {"balance": wallet.balance}
