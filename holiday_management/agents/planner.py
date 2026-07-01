from autogen_agentchat.agents import AssistantAgent
from holiday_management.models.gpt_model import get_model_client

def get_planner_agent():
    """Create and return the planner AssistantAgent using a lazily-created model client."""
    model_client = get_model_client()
    return AssistantAgent(
        name="Holiday_Planner",
        description="A Holiday planner agent that helps users plan their trips.",
        model_client=model_client,
        system_message=(
            "You are a Holiday planner agent. Your task is to help users plan their trips by "
            "providing information about destinations, itineraries, and travel tips."
        ),
    )

# Backwards-compatible export: some modules may still import `planner_agent`.
planner_agent = None