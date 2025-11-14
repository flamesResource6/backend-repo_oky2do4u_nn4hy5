"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category (e.g., Sofa, Table, Chair)")
    in_stock: bool = Field(True, description="Whether product is in stock")
    image_url: Optional[HttpUrl] = Field(None, description="Primary image URL")
    gallery: Optional[List[HttpUrl]] = Field(default_factory=list, description="Additional image URLs")
    tags: Optional[List[str]] = Field(default_factory=list, description="Searchable tags")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating 0-5")
    featured: bool = Field(False, description="Show on homepage highlights")

class Inquiry(BaseModel):
    """
    Customer inquiries/lead collection schema
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Customer name")
    email: EmailStr = Field(..., description="Customer email")
    phone: Optional[str] = Field(None, description="Phone number")
    message: str = Field(..., description="Message from customer")
    product_title: Optional[str] = Field(None, description="Product referenced in inquiry")
    product_id: Optional[str] = Field(None, description="Product id as string if applicable")
