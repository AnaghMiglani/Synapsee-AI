import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

MODE=os.getenv("MODE") or "PRODUCTION"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

