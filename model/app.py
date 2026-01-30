from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agents import extraction_node, validation_node
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Custom reducer to merge dictionaries in state
def merge_dicts(existing: dict, new: dict) -> dict:
    """Merge two dictionaries for LangGraph state updates."""
    return {**existing, **(new if new else {})}


# Define the structure of workflow state
class AgentState(TypedDict):

    # Raw product description
    raw_data: str

    # Path to uploaded image
    image_path: str

    # Extracted product listing
    listing: Annotated[dict, merge_dicts]


# Node for manual review (human-in-the-loop)
def human_review_node(state: AgentState):

    # This node is used only for interruption
    return state


# Initialize the workflow graph
workflow = StateGraph(AgentState)


# Register agent nodes
workflow.add_node("extractor", extraction_node)
workflow.add_node("validator", validation_node)
workflow.add_node("human_review_node", human_review_node)


# Define main workflow path
workflow.add_edge(START, "extractor")
workflow.add_edge("extractor", "validator")


# Decide next step after validation
def route_after_validation(state: AgentState):

    # Send to human review if confidence is low
    if state["listing"].get("requires_manual_review"):
        return "human_review_node"

    # Otherwise, finish workflow
    return END


# Add conditional routing
workflow.add_conditional_edges(
    "validator",
    route_after_validation,
    {
        "human_review_node": "human_review_node",
        END: END
    }
)


# End workflow after human review
workflow.add_edge("human_review_node", END)


# Enable memory-based checkpointing
memory = MemorySaver()


# Compile workflow into executable app
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_review_node"]
)
