# 
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class AccountCreate(BaseModel):
    name: str
    type: str
    balance: Optional[Decimal] = Field(default=0)

class AccountOut(BaseModel):
    id: int
    name: str
    type: str
    balance: Decimal

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    account_id: int
    amount: Decimal
    category: Optional[str] = None
    description: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    account_id: int
    amount: Decimal
    category: Optional[str]
    timestamp: datetime
    description: Optional[str]

    class Config:
        orm_mode = True

class ApiKeyCreate(BaseModel):
    name: Optional[str] = None

class ApiKeyOut(BaseModel):
    key: str
    name: Optional[str]
