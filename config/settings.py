import os
from pathlib import Path
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Document processing
    DOCS_DIR: Path = Field(..., env="DOCS_DIR")
    CHUNK_SIZE: int = Field(512, env="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(50, env="CHUNK_OVERLAP")
    
    # Vector store
    CHROMA_DB_PATH: Path = Field(..., env="CHROMA_DB_PATH")
    EMBEDDING_MODEL: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    COLLECTION_NAME: str = Field("document_qa", env="COLLECTION_NAME")
    HUGGINGFACE_CACHE_PATH: str = Field("", env="HUGGINGFACE_CACHE_PATH")
    
    # Search
    TOP_K: int = Field(5, env="TOP_K")
    CONFIDENCE_THRESHOLD: float = Field(0.7, env="CONFIDENCE_THRESHOLD")
    
    # LLM
    OPENAI_BASE_URL: str = Field("https://api.openai.com/v1", env="OPENAI_BASE_URL")
    OPENAI_MODEL: str = Field("gpt-3.5-turbo", env="OPENAI_MODEL")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FILE: Optional[Path] = Field(None, env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @validator("DOCS_DIR", "CHROMA_DB_PATH", "LOG_FILE", pre=True)
    def validate_paths(cls, v):
        if v is None:
            return v
        return Path(v)

settings = Settings()
os.environ["HF_HOME"] = settings.HUGGINGFACE_CACHE_PATH