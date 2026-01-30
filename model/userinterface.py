import os
import streamlit as st
import pandas as pd

from app import app


# Page configuration
st.set_page_config(
    page_title="Catalog AI",
    layout="wide"
)


# App title
st.title("Multi-Agent Catalog Enrichment System")


# Create two columns: input (left) and output (right)
col1, col2 = st.columns([1, 1])


# Left column: User input
with col1:

    # Product description input
    raw_text = st.text_area(
        "Product Description",
        height=150
    )

    # Product image uploader
    uploaded_file = st.file_uploader(
        "Product Image",
        type=["jpg", "jpeg", "png"]
    )

    # Submit button
    submit_btn = st.button(
        "Enrich Product",
        use_container_width=True
    )


# Run workflow after submission
if submit_btn and raw_text:

    temp_path = None

    # Save uploaded image temporarily
    if uploaded_file:

        temp_dir = "tempDir"
        os.makedirs(temp_dir, exist_ok=True)

        temp_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Preview uploaded image
        st.image(uploaded_file, width=300)


    # Prepare input for LangGraph
    initial_input = {
        "raw_data": raw_text,
        "image_path": temp_path
    }

    # Session configuration
    config = {
        "configurable": {
            "thread_id": "streamlit_demo"
        }
    }


    # Right column: Results
    with col2:

        final_state = None

        # Stream workflow execution
        for event in app.stream(
            initial_input,
            config,
            stream_mode="values"
        ):
            final_state = event


        # Display final output
        if final_state and "listing" in final_state:

            listing = final_state["listing"]


            # Show approval status
            if listing.get("requires_manual_review"):
                st.error("Manual review required")
            else:
                st.success("Listing approved")


            # Basic listing information
            table_rows = [
                ["Title", listing.get("title")],
                ["Category", listing.get("category")],
                ["Confidence", f"{listing.get('confidence_score', 0):.0%}"]
            ]


            # Parse attributes into key-value format
            for attr in listing.get("attributes", []):
                if isinstance(attr, dict):
                    # Use the specific keys 'name' and 'value' defined in your schema
                    name = attr.get("name", "Attribute")
                    value = attr.get("value", "Unknown")
                    table_rows.append([name, value])
                elif ":" in str(attr):
                    # format "Color: Blue"
                    key, val = str(attr).split(":", 1)
                    table_rows.append([key.strip(), val.strip()])


            # Create and display table
            df = pd.DataFrame(table_rows, columns=["Feature", "Details"])

            st.table(df)
