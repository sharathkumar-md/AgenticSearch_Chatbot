from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import DEFAULT_MODEL, DEFAULT_TEMPERATURE
from config.settings import GROQ_MODEL_LIST, GOOGLE_MODEL_LIST

class LLMFactory:
    @staticmethod
    def create_llm(model_name: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE):
        """
        Create an LLM instance based on the model name.
        
        Args:
            model_name: Name of the model to use
            temperature: Temperature parameter for the model
            
        Returns:
            LLM instance
        """
        if model_name in GOOGLE_MODEL_LIST:
            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature
            )
        else:
            return ChatGroq(
                model=model_name,
                temperature=temperature
            )