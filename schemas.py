from enum import Enum

from pydantic import BaseModel, Field, UUID4
from decimal import Decimal

class WalletResponse(BaseModel):
    uuid: UUID4
    balance: Decimal = Field(..., gt=0)

    class Config:
        from_attributes = True

class TypeOperation(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class WalletOperation(BaseModel):
    operation: TypeOperation
    amount: Decimal = Field(..., gt=0)

    class Config:
        from_attributes = True
