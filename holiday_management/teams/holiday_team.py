from autogen_agentchat.teams import RoundRobinGroupChat 
from holiday_management.agents.planner import get_planner_agent
from holiday_management.agents.researcher import get_researcher_agent
from holiday_management.utils.utils import get_termination_condition


def get_team():
    """Create and return the RoundRobinGroupChat team with instantiated agents."""
    planner_agent = get_planner_agent()
    researcher_agent = get_researcher_agent()
    return RoundRobinGroupChat(
        participants=[planner_agent, researcher_agent],
        termination_condition=get_termination_condition(),
        max_turns=6,
    )

# Backwards-compatible export
team = None

