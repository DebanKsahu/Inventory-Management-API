from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import set_page, set_params
from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.ext.sqlmodel import apaginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database.models.entities import Product, ProductIn, ProductUpdate
from app.utils.api_response import APIResponse
from app.utils.dependencies import DependencyContainer

product_router = APIRouter(
    prefix="/products",
    tags=["Product Related Endpoints"]
)

@product_router.post("/", response_model=APIResponse)
async def add_product(product_detail: ProductIn, session: AsyncSession = Depends(DependencyContainer.get_session)):
    session.add(Product(
        name=product_detail.name,
        description=product_detail.description,
        price=product_detail.price,
        available_quantity=product_detail.available_quantity
    ))
    await session.commit()
    return APIResponse.successful_response(message=f"Product {product_detail.name} is successfully added")

@product_router.get("/", response_model=APIResponse)
async def show_products(params: CursorParams = Depends(), session: AsyncSession = Depends(DependencyContainer.get_session)):
    set_page(CursorPage[Product])
    pages = await apaginate(session,select(Product).order_by(Product.id),params=params) # type: ignore
    return APIResponse.successful_response(data=pages, message="Products successfully retrieved")

@product_router.get("/{id}", response_model=APIResponse)
async def get_product_detail(id: int, session: AsyncSession = Depends(DependencyContainer.get_session)):
    product_detail = await session.get(Product,id)
    if product_detail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIResponse.unsuccessful_response(message="Product Not Found").model_dump()
        )
    else:
        return APIResponse.successful_response(data=product_detail,message="Product successfuly retrieved")

@product_router.put("/{id}", response_model=APIResponse)
async def update_product_detail(id: int, new_product_details: ProductUpdate, session: AsyncSession = Depends(DependencyContainer.get_session)):
    new_product_details_dict = new_product_details.model_dump(exclude_unset=True)
    query = select(Product).where(Product.id==id).with_for_update()
    existing_product = (await session.execute(query)).scalar_one_or_none()
    if existing_product is not None:
        for key,value in new_product_details_dict.items():
            match key:
                case "name":
                    existing_product.name = value
                case "description":
                    existing_product.description = value
                case "price":
                    existing_product.price = value
                case "available_quantity":
                    existing_product.available_quantity = value
        session.add(existing_product)
        await session.commit()
        return APIResponse.successful_response(message="Product detail successfuly updated")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIResponse.unsuccessful_response(message="Product Not Found").model_dump()
        )

@product_router.delete("/{id}", response_model=APIResponse)
async def delete_product(id: int, session: AsyncSession = Depends(DependencyContainer.get_session)):
    existing_product = await session.get(Product,id)
    if existing_product is not None:
        await session.delete(existing_product)
        await session.commit()
        return APIResponse.successful_response(message="Product deletion successfuly completed")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIResponse.unsuccessful_response(message="Product Not Found").model_dump()
        )