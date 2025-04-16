from pydantic import BaseModel, Field
## This example to show pydantic validation only using Postman
class Review(BaseModel):
    review_id: str = Field(..., description="Unique identifier for the review")
    rating: int = Field(..., ge=1, le=5, description="Rating of the product (1 to 5)")
    review_text: str = Field(..., description="Comments on the product")
    review_title: str = Field(..., description="title of the review")