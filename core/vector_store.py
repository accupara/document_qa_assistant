import logging
import chromadb
from typing import List, Dict, Optional, Tuple
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
from ..config.settings import settings

logger = logging.getLogger(__name__)

class VectorStore:
    """Handles all operations with the ChromaDB vector store."""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(settings.CHROMA_DB_PATH),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL
        )
        
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get existing collection or create a new one."""
        try:
            collection = self.client.get_collection(
                name=settings.COLLECTION_NAME,
                embedding_function=self.embedding_function
            )
            logger.info(f"Using existing collection: {settings.COLLECTION_NAME}")
            return collection
        except ValueError:
            logger.info(f"Creating new collection: {settings.COLLECTION_NAME}")
            return self.client.create_collection(
                name=settings.COLLECTION_NAME,
                embedding_function=self.embedding_function
            )
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store."""
        if not documents:
            logger.warning("No documents to add to vector store.")
            return
        
        ids = [str(i) for i in range(len(documents))]
        embeddings = [doc.metadata["embedding"] for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        contents = [doc.page_content for doc in documents]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=contents
        )
        logger.info(f"Added {len(documents)} documents to vector store")
    
    def query(self, query_text: str, top_k: Optional[int] = None) -> List[Tuple[str, float]]:
        """Query the vector store for similar documents."""
        top_k = top_k or settings.TOP_K
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        
        # Format results as (document, score) pairs
        documents = results["documents"][0]
        scores = results["distances"][0]
        metadatas = results["metadatas"][0]
        
        return list(zip(documents, scores, metadatas))
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        self.collection.delete()
        logger.info("Cleared vector store collection")