from typing import List
from pydantic import BaseModel, Field


# Pydantic model for individual product attributes
class Attribute(BaseModel):
    name: str = Field(description="The specific name of the property, like 'Fabric', 'Color', or 'Caffeine Content'")
    value: str = Field(description="The value of that property")



# Pydantic model for structured product data
class ProductListing(BaseModel):

    # Standardized product title
    title: str = Field(
        description="Standardized product title"
    )

    # List of extracted attributes (color, size, material, etc.)
    attributes: List[Attribute] = Field(
        description="List of specific features found in the product"
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
