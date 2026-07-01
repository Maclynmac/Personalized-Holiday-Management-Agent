import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present) before reading them
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_MOCK_MODEL = os.getenv("USE_MOCK_MODEL", "false").strip().lower() in ("1", "true", "yes")
MODEL_NAME = "gpt-4o-mini"