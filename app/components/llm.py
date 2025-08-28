from langchain_groq import ChatGroq
from app.config.config import GROQ_API_KEY

from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger = get_logger(__name__)


def load_llm(
    model_name: str = "llama-3.1-8b-instant",
    groq_api_key: str = GROQ_API_KEY,
    temperature: float = 0.3,
    max_tokens: int = 256,
) -> ChatGroq:
    """
    Load ChatGroq LLM, with specified hyperparameters.
    """
    logger.info("Loading LLM from Groq using llama3 model...")

    try:
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        logger.info("LLM loaded successfully...")

        return llm

    except Exception as e:
        error_message = CustomException("Failed to load LLM", e)
        logger.error(str(error_message))
