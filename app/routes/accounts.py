# app/routes/accounts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from typing import List
from ..schemas import AccountCreate, AccountOut, ApiKeyOut, ApiKeyCreate
from ..models import Account, ApiKey
from ..database import get_db, AsyncSessionLocal
from ..auth import get_api_key, require_master_key, generate_api_key
from sqlalchemy.exc import NoResultFound

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
async def create_account(payload: AccountCreate, session: AsyncSession = Depends(get_db), _=Depends(get_api_key)):
    account = Account(name=payload.name, type=payload.type, balance=payload.balance)
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account

@router.get("", response_model=List[AccountOut])
async def list_accounts(session: AsyncSession = Depends(get_db), _=Depends(get_api_key)):
    q = select(Account)
    res = await session.execute(q)
    accounts = res.scalars().all()
    return accounts

@router.get("/{account_id}", response_model=AccountOut)
async def get_account(account_id: int, session: AsyncSession = Depends(get_db), _=Depends(get_api_key)):
    q = select(Account).where(Account.id == account_id)
    res = await session.execute(q)
    account = res.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

# Admin: create API key (protected by MASTER API key)
@router.post("/keys", response_model=ApiKeyOut)
async def create_api_key(payload: ApiKeyCreate, _=Depends(require_master_key)):
    key_str = generate_api_key()
    async with AsyncSessionLocal() as session:
        api_key = ApiKey(key=key_str, name=payload.name)
        session.add(api_key)
        await session.commit()
        await session.refresh(api_key)
        return {"key": api_key.key, "name": api_key.name}
