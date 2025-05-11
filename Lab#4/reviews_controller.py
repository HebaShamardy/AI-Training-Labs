from fastapi import HTTPException, status, Depends
from typing import List
from pymongo.errors import PyMongoError
from fastapi import APIRouter
from review import Review
from mongodb import get_database

router = APIRouter()


# --- Review Endpoints ---

@router.post("/reviews/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(review: Review, db = Depends(get_database)):
    """
    Create a new review.
    """
    try:
        reviews_collection = db.reviews
        products_collection = db.products #check if product exists
        product = products_collection.find_one({"product_id": review.product_id})
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID is invalid")

        existing_review = reviews_collection.find_one({"review_id": review.review_id})
        if existing_review:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Review with this ID already exists")

        result = reviews_collection.insert_one(review.model_dump())
        if result.inserted_id:
             # Fetch the inserted review to ensure correct structure and return
            inserted_review = reviews_collection.find_one({"_id": result.inserted_id})
            return Review(**inserted_review)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create review")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

@router.get("/reviews/{review_id}", response_model=Review)
async def get_review(review_id: str, db = Depends(get_database)):
    """
    Get a review by its ID.
    """
    try:
        reviews_collection = db.reviews
        review_data = reviews_collection.find_one({"review_id": review_id})
        if review_data:
            return Review(**review_data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

@router.put("/reviews/{review_id}", response_model=Review)
async def update_review(review_id: str, review: Review, db = Depends(get_database)):
    """
    Update a review by its ID.
    """
    try:
        reviews_collection = db.reviews
        existing_review = reviews_collection.find_one({"review_id": review_id})
        if not existing_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        result = reviews_collection.replace_one({"review_id": review_id}, review.dict())
        if result.modified_count > 0:
             # Fetch the updated review
            updated_review = reviews_collection.find_one({"review_id": review_id})
            return Review(**updated_review)
        else:
            return Review(**existing_review)
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: str, db = Depends(get_database)):
    """
    Delete a review by its ID.
    """
    try:
        reviews_collection = db.reviews
        result = reviews_collection.delete_one({"review_id": review_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return None
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

@router.get("/reviews/", response_model=List[Review])
async def get_all_reviews(skip: int = 0, limit: int = 10, db = Depends(get_database)):
    """
    Get all reviews with pagination.
    """
    try:
        reviews_collection = db.reviews
        reviews = list(reviews_collection.find().skip(skip).limit(limit))
        return [Review(**review) for review in reviews]
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
    


@router.get("/products/{product_id}/reviews", response_model=List[Review])
async def get_reviews_for_product(product_id: str, db = Depends(get_database)):
    """
    Get all reviews for a specific product.
    """
    try:
        reviews_collection = db.reviews
        products_collection = db.products
        product = products_collection.find_one({"product_id": product_id})
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID is invalid")
        reviews = list(reviews_collection.find({"product_id": product_id}))
        return [Review(**review) for review in reviews]
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
