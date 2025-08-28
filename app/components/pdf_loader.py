import os

from typing import List

from langchain.schema.document import Document
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP


logger = get_logger(__name__)


def load_pdf_files() -> List[Document]:
    if not os.path.exists(DATA_PATH):
        raise CustomException

    logger.info(f"Loading files from {DATA_PATH}...")
    try:
        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()

        if not documents:
            logger.warning("No PDFs found")
        else:
            logger.info(f"Successfully loaded {len(documents)} documents")

        return documents

    except Exception as e:
        error_message = CustomException("Failed to load PDFs", e)
        logger.error(str(error_message))
        return []


def create_text_chunks(documents: List[Document]) -> List[str]:
    if not documents:
        raise CustomException("No documents found")

    logger.info(f"Splitting {len(documents)}...")

    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )

        text_chunks = text_splitter.split_documents(documents)
        logger.info(f"Generated {len(text_chunks)} text chunks")
        return text_chunks

    except Exception as e:
        error_message = CustomException("Failed to generate text chunks", e)
        logger.error(str(error_message))
        return []
