import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

MODE=os.getenv("MODE") or "PRODUCTION"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

