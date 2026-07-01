from autogen_agentchat.agents import AssistantAgent
from holiday_management.models.gpt_model import get_model_client

def get_researcher_agent():
    """Create and return the researcher AssistantAgent using a lazily-created model client."""
    model_client = get_model_client()
    return AssistantAgent(
        name="Holiday_Researcher",
        description=(
            "A Holiday researcher agent that helps users research about their holiday destinations."
        ),
        model_client=model_client,
        system_message=(
            "You are a Holiday researcher agent. Your task is to help users research about their "
            "holiday destinations by providing information about attractions, local culture, and travel tips."
        ),
    )

# Backwards-compatible export
researcher_agent = None