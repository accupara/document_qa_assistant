import pytest
from core.vector_store import VectorStore

@pytest.fixture
def vector_store():
    return VectorStore()

def test_add_documents(vector_store):
    # Test adding documents to the vector store
    pass

def test_query(vector_store):
    # Test querying the vector store
    pass