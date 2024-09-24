import uuid

from sqlalchemy import Column, Integer, DECIMAL
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()

class WalletModel(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    balance = Column(DECIMAL(precision=10, scale=2), default=0.00)