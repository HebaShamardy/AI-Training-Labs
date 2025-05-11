from pydantic import BaseModel, Field

class Review(BaseModel):
    review_id: str = Field(..., description="Unique identifier for the review")
    review_title: str = Field(..., description="Title of the review")
    review_text: str = Field(..., description="Comments on the product")
    product_rating: int = Field(..., ge=1, le=5, description="Rating of the product (1 to 5)")
    product_id: str = Field(..., description="identifier for the product")
    product_name: str = Field(..., description="Name of the reviewed product")
    product_description: str = Field(..., description="Description of the reviewed product")
