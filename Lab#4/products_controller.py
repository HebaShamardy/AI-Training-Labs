from fastapi import HTTPException, status, Depends
from typing import List
from pymongo.errors import PyMongoError
from fastapi import APIRouter
from product import Product
from mongodb import get_database

router = APIRouter()

# --- Product Endpoints ---

@router.post("/products/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product, db = Depends(get_database)):
    """
    Create a new product.
    """
    try:
        products_collection = db.products
        existing_product = products_collection.find_one({"product_id": product.product_id})
        if existing_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this ID already exists")
        result = products_collection.insert_one(product.model_dump())
        if result.inserted_id:
            # Fetch the inserted product to ensure correct structure and return
            inserted_product = products_collection.find_one({"_id": result.inserted_id})
            return Product(**inserted_product)  # Use the Pydantic model for response
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str, db = Depends(get_database)):
    """
    Get a product by its ID.
    """
    try:
        products_collection = db.products
        print("Daamn ", {"product_id": product_id})
        product_data = products_collection.find_one({"product_id": product_id})
        if product_data:
            return Product(**product_data)  # Use the Pydantic model
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: Product, db = Depends(get_database)):
    """
    Update a product by its ID.
    """
    try:
        products_collection = db.products
        existing_product = products_collection.find_one({"product_id": product_id})
        if not existing_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        result = products_collection.replace_one({"product_id": product_id}, product.model_dump())
        if result.modified_count > 0:
            # Fetch the updated product
            updated_product = products_collection.find_one({"product_id": product_id})
            return Product(**updated_product) # Return updated product
        else:
            # Handle the case where the product exists, but no fields were actually modified.
             return Product(**existing_product) # Return the existing product
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, db = Depends(get_database)):
    """
    Delete a product by its ID.
    """
    try:
        products_collection = db.products
        result = products_collection.delete_one({"product_id": product_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return None  # 204 No Content - success, no content to return
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

@router.get("/products/", response_model=List[Product])
async def get_all_products(skip: int = 0, limit: int = 10, db = Depends(get_database)):
    """
    Get all products with pagination.
    """
    try:
        print("Hi")
        products_collection = db.products
        products = list(products_collection.find().skip(skip).limit(limit))
        return [Product(**product) for product in products]
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

