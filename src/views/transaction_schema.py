from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.domain.transaction import Transaction


class TransactionSchema(Transaction):
    pass


class TransactionCreateSchema(BaseModel):
    amount: float
    description: str
    date: date
    category: str
    tags: Optional[list[str]]


class TransactionUpdateSchema(BaseModel):
    amount: Optional[float]
    description: Optional[str]
    date: Optional[date]
    category: Optional[str]
