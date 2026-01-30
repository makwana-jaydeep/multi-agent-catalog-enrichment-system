import os
import base64
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from schema import ProductListing


# Load environment variables (API keys, configs)
load_dotenv()


# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Configure LLM to return structured output
structured_llm = llm.with_structured_output(ProductListing)


# Convert image to base64 format
def encode_image(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Agent node: Extract structured data from text and image
def extraction_node(state):

    # Get input values from state
    raw_text = state.get("raw_data", "")
    image_path = state.get("image_path")


    # System prompt for guiding the model
    system_prompt = SystemMessage(
        content=(
            "You are a product catalog specialist. Your task is to extract structured product data. "
            "If an image is provided, treat it as the primary source of truth. "
            "If the text description contradicts the image, "
            "set 'requires_manual_review' to True and reduce the 'confidence_score'."
        )
    )


    # Prepare text input for the model
    content = [
        {
            "type": "text",
            "text": f"Text Description: {raw_text}"
        }
    ]


    # Add image input if available
    if image_path:

        with open(image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode("utf-8")

        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        )


    # Create message for LLM
    message = HumanMessage(content=content)


    # Call model to extract structured data
    enriched_data = structured_llm.invoke([system_prompt, message])


    # Return extracted listing
    return {
        "listing": enriched_data.model_dump()
    }


# Agent node: Validate extracted data
def validation_node(state):

    # Get listing from state
    listing = state.get("listing", {})


    # Basic validation: check title length
    if len(listing.get("title", "")) < 10:
        listing["requires_manual_review"] = True


    # Return updated state
    return {
        "listing": listing
    }
