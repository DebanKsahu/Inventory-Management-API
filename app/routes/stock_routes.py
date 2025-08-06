from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import set_page, set_params
from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlmodel import apaginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.models.entities import Product, StockTransaction, StockTransactionIn
from app.utils.api_response import APIResponse
from app.utils.dependencies import DependencyContainer
from app.utils.enums import TransactionType

stock_router = APIRouter(
    prefix="/stock",
    tags=["Stock related endpoint"]
)

@stock_router.post("/", response_model=APIResponse)
async def add_stock_transaction(transaction_detail: StockTransactionIn, session: AsyncSession = Depends(DependencyContainer.get_session)):
    query = select(Product).where(Product.id==transaction_detail.product_id).with_for_update()
    product_detail = (await session.execute(query)).scalar_one_or_none()
    if product_detail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIResponse.unsuccessful_response(message="Product not found, can't create transaction if product is not present")
        )
    else:
        if transaction_detail.quantity>product_detail.available_quantity and transaction_detail.transaction_type==TransactionType.OUT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=APIResponse.unsuccessful_response(message=f"Requested amount not available. Currenly only {product_detail.available_quantity} product available")
            )
        else:
            stock_transaction = StockTransaction(
                product_id=transaction_detail.product_id,
                quantity=transaction_detail.quantity,
                transaction_type=transaction_detail.transaction_type,
            )
            if (transaction_detail.transaction_type==TransactionType.OUT):
                product_detail.available_quantity -= transaction_detail.quantity
            else:
                product_detail.available_quantity += transaction_detail.quantity

            session.add(stock_transaction)
            session.add(product_detail)
        await session.commit()
        return APIResponse.successful_response(message="Transaction successfuly added")

@stock_router.get("/", response_model=APIResponse)
async def all_transactions(params: CursorParams = Depends(), session: AsyncSession = Depends(DependencyContainer.get_session)):
    set_page(CursorPage[StockTransaction])
    pages = await apaginate(session, select(StockTransaction).order_by(StockTransaction.id),params=params) #type: ignore
    return APIResponse.successful_response(data = pages, message="Transactions successfullt retrieved")

@stock_router.get("/product/{product_id}", response_model=APIResponse)
async def get_product_transactions(product_id: int, params: CursorParams = Depends(), session: AsyncSession = Depends(DependencyContainer.get_session)):
    product_detail = await session.get(Product,product_id)
    if product_detail is not None:
        set_page(CursorPage[StockTransaction])
        pages = await apaginate(session, select(StockTransaction).where(StockTransaction.product_id==product_id).order_by(StockTransaction.id),params=params) #type: ignore
        return APIResponse.successful_response(data = pages, message="All transaction of the product retrieved")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIResponse.unsuccessful_response(message="Product Not Found").model_dump()
        )