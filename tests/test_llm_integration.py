import pytest
from core.llm_integration import LLMIntegration

@pytest.fixture
def llm_integration():
    return LLMIntegration()

def test_generate_response(llm_integration):
    # Test response generation (mock API calls)
    pass