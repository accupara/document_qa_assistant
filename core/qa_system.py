import logging
from typing import List, Tuple, Generator
from config.settings import settings
from .document_processor import DocumentProcessor
from .vector_store import VectorStore
from .llm_integration import LLMIntegration

logger = logging.getLogger(__name__)

class QASystem:
    """Main QA system that orchestrates document processing, search, and answer generation."""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.llm = LLMIntegration()
        
        # Initialize the system
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize the vector store with documents if empty."""
        if self.vector_store.collection.count() == 0:
            logger.info("Vector store is empty, processing documents...")
            documents = self.document_processor.process_all_documents()
            self.vector_store.add_documents(documents)
    
    def search_documents(self, query: str) -> List[Tuple[str, float, dict]]:
        """Search for relevant documents in the vector store."""
        results = self.vector_store.query(query)
        
        # Filter by confidence threshold
        filtered_results = [
            (doc, score, metadata)
            for doc, score, metadata in results
            if score >= settings.CONFIDENCE_THRESHOLD
        ]
        
        if not filtered_results:
            logger.warning(f"No documents found above confidence threshold {settings.CONFIDENCE_THRESHOLD}")
        
        return filtered_results
    
    def format_citations(self, results: List[Tuple[str, float, dict]]) -> str:
        """Format search results for display."""
        formatted = []
        for i, (doc, score, metadata) in enumerate(results, 1):
            source = metadata.get("source", "Unknown source")
            page = metadata.get("page", "")
            citation = f"[{i}] {source}"
            if page:
                citation += f" (page {page})"
            citation += f" - Confidence: {score:.2f}"
            formatted.append(citation)
        
        return "\n".join(formatted)
    
    def generate_answer(
        self,
        question: str,
        context: str
    ) -> Generator[str, None, None]:
        """Generate an answer to the question using the provided context."""
        return self.llm.generate_response(question, context)
    
    def answer_question(self, question: str) -> Tuple[str, str]:
        """Full QA pipeline: search, format citations, generate answer."""
        # Step 1: Semantic search
        search_results = self.search_documents(question)
        citations = self.format_citations(search_results)
        
        # Step 2: Build context
        context = "\n\n".join([
            f"Document {i}:\n{doc}"
            for i, (doc, _, _) in enumerate(search_results, 1)
        ])
        
        # Step 3: Generate answer
        answer_stream = self.generate_answer(question, context)
        
        return answer_stream, citations