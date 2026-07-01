from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import CreateResult
from autogen_core.models._types import RequestUsage
from holiday_management.config.settings import OPENAI_API_KEY, MODEL_NAME, USE_MOCK_MODEL
from dotenv import load_dotenv
from openai import OpenAIError
import os

load_dotenv()

_client = None


class MockModelClient:
    async def create(self, *args, **kwargs):
        return CreateResult(
            finish_reason="stop",
            content=(
                "OpenAI quota is unavailable. This is a fallback response from the local "
                "mock client. To use the real model again, restore your OpenAI quota or "
                "switch to a valid API key."
            ),
            usage=RequestUsage(prompt_tokens=0, completion_tokens=0),
            cached=False,
        )

    async def create_stream(self, *args, **kwargs):
        yield await self.create(*args, **kwargs)


class SafeOpenAIClient:
    def __init__(self, client):
        self._client = client

    def __getattr__(self, name):
        return getattr(self._client, name)

    async def create(self, *args, **kwargs):
        try:
            return await self._client.create(*args, **kwargs)
        except OpenAIError as e:
            print(f"OpenAI client error: falling back to local mock model. ({type(e).__name__})")
            return await MockModelClient().create(*args, **kwargs)

    async def create_stream(self, *args, **kwargs):
        try:
            stream = self._client.create_stream(*args, **kwargs)
            if hasattr(stream, "__aiter__"):
                async for chunk in stream:
                    yield chunk
            else:
                stream = await stream
                async for chunk in stream:
                    yield chunk
        except OpenAIError as e:
            print(f"OpenAI client error: falling back to local mock model. ({type(e).__name__})")
            yield await MockModelClient().create(*args, **kwargs)
            return


def get_model_client():
    """Lazily create and return the OpenAIChatCompletionClient wrapper."""
    global _client
    if _client is not None:
        return _client

    api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_ADMIN_KEY")
    if USE_MOCK_MODEL:
        return MockModelClient()

    if not api_key:
        print(
            "OpenAI API key not found. Falling back to mock model. "
            "Set OPENAI_API_KEY or OPENAI_ADMIN_KEY to use the live OpenAI API."
        )
        return MockModelClient()

    client = OpenAIChatCompletionClient(model=MODEL_NAME, openai_api_key=api_key)
    _client = SafeOpenAIClient(client)
    return _client


# Backwards-compatible export in case other code imports model_client directly.
model_client = None
