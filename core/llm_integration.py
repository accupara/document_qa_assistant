import logging
from typing import Generator, Optional
import openai
from ..config.settings import settings

logger = logging.getLogger(__name__)

class LLMIntegration:
    """Handles interactions with the OpenAI-compatible API."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        openai.api_base = settings.OPENAI_BASE_URL
        
        # Validate connection
        try:
            models = openai.Model.list()
            logger.debug(f"Available models: {[m['id'] for m in models['data']]}")
        except Exception as e:
            logger.error(f"Failed to connect to LLM API: {str(e)}")
            raise
    
    def generate_response(
        self,
        prompt: str,
        context: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Generator[str, None, None]:
        """Generate a streaming response from the LLM."""
        full_prompt = f"""
        Context information is below.
        ---------------------
        {context}
        ---------------------
        Given the context information and not prior knowledge, answer the query.
        Query: {prompt}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in response:
                content = chunk["choices"][0].get("delta", {}).get("content", "")
                if content:
                    yield content
        
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            yield f"Error: {str(e)}"