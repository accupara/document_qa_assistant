import pytest
from pathlib import Path
from core.document_processor import DocumentProcessor
from config.settings import settings

@pytest.fixture
def doc_processor():
    return DocumentProcessor()

def test_load_documents(doc_processor):
    # Setup test documents in a temporary directory
    # Test loading different file types
    pass

def test_split_documents(doc_processor):
    # Test document splitting with various chunk sizes
    pass

def test_embed_text(doc_processor):
    # Test embedding generation
    pass