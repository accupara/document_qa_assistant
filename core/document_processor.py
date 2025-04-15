import logging
from pathlib import Path
from typing import Any, List, Optional, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    UnstructuredFileLoader,
    UnstructuredWordDocumentLoader,
    PyPDFLoader
)
from sentence_transformers import SentenceTransformer, util as stutil
from transformers import file_utils
from config.settings import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document loading, splitting, and embedding."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len
        )
        # stutil.HUGGINGFACE_HUB_CACHE = settings.HUGGINGFACE_CACHE_PATH
        print(file_utils.default_cache_path)
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    def load_documents(self) -> List[Dict[str, Any]]:
        """Load and process all documents from the specified directory."""
        documents = []
        supported_extensions = {
            ".md": UnstructuredMarkdownLoader,
            ".pdf": PyPDFLoader,
            ".doc": UnstructuredWordDocumentLoader,
            ".docx": UnstructuredWordDocumentLoader
        }
        
        for ext, loader_class in supported_extensions.items():
            for file_path in settings.DOCS_DIR.glob(f"*{ext}"):
                try:
                    logger.info(f"Processing file: {file_path}")
                    loader = loader_class(str(file_path))
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {str(e)}")
                    continue
        
        return documents
    
    def split_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Split documents into chunks."""
        return self.text_splitter.split_documents(documents)
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for a text chunk."""
        return self.embedding_model.encode(text).tolist()
    
    def process_all_documents(self) -> List[Dict[str, Any]]:
        """Full pipeline: load, split, and embed all documents."""
        raw_documents = self.load_documents()
        if not raw_documents:
            logger.warning("No documents found in the specified directory.")
            return []
        
        split_documents = self.split_documents(raw_documents)
        logger.info(f"Split documents into {len(split_documents)} chunks")
        
        # Add embeddings to each document
        for doc in split_documents:
            doc.metadata["embedding"] = self.embed_text(doc.page_content)
        
        return split_documents