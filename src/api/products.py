from fastapi import APIRouter, HTTPException
from typing import List

from src.services.product_service import ProductService
from src.models.product import Product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


product_service = ProductService()


# Get all products

@router.get("/")
async def get_products():

    products = await product_service.get_all_products()

    return {
        "status": "success",
        "count": len(products),
        "products": products
    }



# Search product

@router.get("/search")
async def search_products(
    query: str
):

    products = await product_service.search_products(
        query
    )

    return {
        "status": "success",
        "query": query,
        "results": products
    }



# Get single product

@router.get("/{product_id}")
async def get_product(
    product_id: str
):

    product = await product_service.get_product_by_id(
        product_id
    )


    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    return {
        "status": "success",
        "product": product
    }



# Check stock

@router.get("/{product_id}/stock")
async def check_stock(
    product_id: str
):

    stock = await product_service.check_stock(
        product_id
    )


    return {
        "product_id": product_id,
        "stock": stock
    }



# Add new product (Admin)

@router.post("/")
async def create_product(
    product: Product
):

    result = await product_service.create_product(
        product
    )


    return {
        "status": "created",
        "product": result
    }



# Update product (Admin)

@router.put("/{product_id}")
async def update_product(
    product_id: str,
    product: Product
):

    result = await product_service.update_product(
        product_id,
        product
    )


    if not result:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    return {
        "status": "updated",
        "product": result
    }



# Delete product (Admin)

@router.delete("/{product_id}")
async def delete_product(
    product_id: str
):

    result = await product_service.delete_product(
        product_id
    )


    if not result:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    return {
        "status": "deleted",
        "product_id": product_id
    }