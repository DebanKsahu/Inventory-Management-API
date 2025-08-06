from datetime import datetime, timezone
from typing import List
from sqlmodel import Relationship, SQLModel, Field

from app.utils.enums import TransactionType

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    price: float = Field(ge=0.0)
    available_quantity: int = Field(ge=0.0)

    product_transactions: List["StockTransaction"] = Relationship(back_populates="product_detail", cascade_delete=True)

class ProductIn(SQLModel):
    name: str 
    description: str 
    price: float 
    available_quantity: int 

class ProductUpdate(SQLModel):
    name: str | None = Field(default=None,min_length=1)
    description: str | None = Field(default=None,min_length=1)
    price: float | None = Field(default=None,ge=0.0)
    available_quantity: int | None = Field(default=None,ge=0.0)

class StockTransaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(ge=1, foreign_key="product.id")
    quantity: int = Field(ge=0)
    transaction_type: TransactionType
    timestamp: datetime | None = Field(default_factory=lambda : datetime.now(timezone.utc))

    product_detail: Product = Relationship(back_populates="product_transactions")

class StockTransactionIn(SQLModel):
    product_id: int 
    quantity: int 
    transaction_type: TransactionType