import asyncio
import subprocess
import sys


def ensure_autogen_dependencies():
    try:
        from autogen_agentchat.messages import TextMessage  # noqa: F401
    except ModuleNotFoundError:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--user",
                "autogen-agentchat",
                "autogen-ext[openai]",
            ]
        )


try:
    from autogen_agentchat.messages import TextMessage
except ModuleNotFoundError:
    ensure_autogen_dependencies()
    from autogen_agentchat.messages import TextMessage

from holiday_management.teams.holiday_team import get_team


async def main():
    task = TextMessage(
        content="I want to plan a trip to Paris for 5 days. Can you help me with that?",
        source="User",
    )
    team = get_team()
    try:
        response = await team.run(task=task)
    except Exception as e:
        print("Error during agent execution:", e)
        if "insufficient_quota" in str(e) or "RateLimitError" in type(e).__name__:
            print(
                "Your OpenAI key has insufficient quota or hit a rate limit. "
                "Check your OpenAI plan and billing details."
            )
        return

    for message in response.messages:
        print(f"{message.source}: {message.content}")


if __name__ == "__main__":
    asyncio.run(main())
