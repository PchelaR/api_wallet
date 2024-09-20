from pydantic import BaseModel, Field, UUID4
from decimal import Decimal

class WalletResponse(BaseModel):
    uuid: UUID4
    balance: Decimal = Field(..., gt=0)

    class Config:
        from_attributes = True


class WalletOperation(BaseModel):
    operation: str
    amount: Decimal = Field(..., gt=0)

    class Config:
        from_attributes = True

