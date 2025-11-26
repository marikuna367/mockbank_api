from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from decimal import Decimal
from ..schemas import TransactionCreate, TransactionOut
from ..models import Transaction, Account
from ..database import get_db
from ..auth import get_api_key
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=TransactionOut, status_code=201)
async def add_transaction(payload: TransactionCreate, session: AsyncSession = Depends(get_db), _=Depends(get_api_key)):
    # Verify account exists
    q = select(Account).where(Account.id == payload.account_id)
    res = await session.execute(q)
    account = res.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    tx = Transaction(
        account_id=payload.account_id,
        amount=payload.amount,
        category=payload.category,
        description=payload.description
    )

    session.add(tx)
    # update account balance
    # Decimal arithmetic
    account.balance = account.balance + payload.amount
    session.add(account)

    await session.commit()
    await session.refresh(tx)
    return tx

@router.get("", response_model=List[TransactionOut])
async def list_transactions(
    account_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db),
    _=Depends(get_api_key),
):
    q = select(Transaction)
    filters = []
    if account_id is not None:
        filters.append(Transaction.account_id == account_id)
    if category:
        filters.append(Transaction.category == category)
    if date_from:
        filters.append(Transaction.timestamp >= date_from)
    if date_to:
        filters.append(Transaction.timestamp <= date_to)
    if filters:
        q = q.where(and_(*filters))
    q = q.order_by(Transaction.timestamp.desc()).limit(limit).offset(offset)
    res = await session.execute(q)
    txs = res.scalars().all()
    return txs
