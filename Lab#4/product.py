from pydantic import BaseModel, Field

class Product(BaseModel):
    product_id: str = Field(..., description="Unique identifier for the product")
    name: str = Field(..., description="Name of the product")
    description: str = Field(..., description="Description of the product")
    price: float = Field(..., gt=0, description="Price of the product (must be greater than 0)")
    category: str = Field(..., description="Category of the product")
    inventory_count: int = Field(..., ge=0, description="Inventory count (must be non-negative)")