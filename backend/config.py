import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "")
    LLAMA_API_KEY = os.getenv("LLAMA_API_KEY", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"