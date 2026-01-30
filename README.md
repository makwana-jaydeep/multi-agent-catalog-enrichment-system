# Multi-Agent Catalog Enrichment System

This project is an AI-powered pipeline designed to automate the extraction,
standardization, and validation of product catalog data. It uses multi-modal
language models and agent-based workflows to convert unstructured seller inputs
into high-quality, structured listings while identifying potential risks and
inconsistencies.


## Overview

The system follows a multi-agent architecture to manage complex retail data
workflows. It processes both textual descriptions and product images to maintain
catalog accuracy and consistency.

A dedicated validation agent compares visual inputs with textual descriptions
to detect mismatches and potential compliance issues. When inconsistencies are
detected, the system flags the listing for further review.


## Key Features

- Multi-modal Analysis  
  Extracts product attributes from both images and text using GPT-4o-mini.

- Agent-based Orchestration  
  Uses LangGraph to manage stateful workflows and agent interactions.

- Automated Risk Detection  
  Identifies inconsistencies between visual and textual data and adjusts
  confidence scores accordingly.

- Human-in-the-Loop Support  
  Triggers manual review for low-confidence or high-risk listings.

- Structured Output  
  Enforces a strict Pydantic schema to produce machine-readable data.


## Technology Stack

- Frameworks: LangChain, LangGraph
- Models: OpenAI GPT-4o-mini
- Interface: Streamlit
- Validation: Pydantic v2
- Language: Python 3.10+


## Project Structure

- userinterface.py   — Streamlit dashboard
- app.py             — Workflow and state management
- agents.py          — Agent logic
- schema.py          — Data models
- requirements.txt   — Dependencies


## Installation

1. Clone the repository.

2. Create a .env file in the root directory:

   ```OPENAI_API_KEY=your_api_key_here```

3. Install dependencies:

   ```pip install -r requirements.txt```


## Usage

Run the application with:

   ```streamlit run userinterface.py```

Upload a product image and provide a text description. The system will generate
a structured output including title, category, confidence score, and attributes.


## Implementation Details

The workflow uses a custom state reducer to merge data across nodes.
Pydantic's model_dump method ensures consistent JSON serialization.

If a listing requires manual verification, execution is paused and control
is transferred to a human reviewer, enabling seamless collaboration between
automated agents and operators.
