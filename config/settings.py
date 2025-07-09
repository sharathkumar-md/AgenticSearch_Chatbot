import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Model configurations
GROQ_MODEL_LIST = [
    "llama-3.2-90b-vision-preview",
    "llama-3.2-11b-vision-preview",
    "llama-3.2-3b-preview",
    "llama-3.2-1b-preview",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "gemma-7b-it",
    "llama3-groq-70b-8192-tool-use-preview",
    "llama3-groq-8b-8192-tool-use-preview",
    "llama-guard-3-8b",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768"
]

GOOGLE_MODEL_LIST = [
    "gemini-1.5-flash-002",
    "gemini-1.5-pro-002",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.5-flash-8b",
]

# # Default configurations
DEFAULT_MODEL = "llama-3.2-90b-vision-preview"
DEFAULT_TEMPERATURE = 0.5