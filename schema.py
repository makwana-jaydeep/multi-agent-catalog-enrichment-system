from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Pydantic model for structured product data
class ProductListing(BaseModel):

    # Standardized product title
    title: str = Field(
        description="Standardized product title"
    )

    # List of extracted attributes (color, size, material, etc.)
    attributes: List[str] = Field(
        description="Extracted product attributes like color, size, material"
    )

    # Product category
    category: str = Field(
        description="Category name"
    )

    # Confidence score (0 to 1)
    confidence_score: float = Field(
        description="Confidence score between 0 and 1",
        ge=0,
        le=1
    )

    # Flag for manual review
    requires_manual_review: bool = Field(
        default=False
    )
