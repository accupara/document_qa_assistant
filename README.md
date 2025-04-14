# Document QA Assistant

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A robust pipeline for document ingestion, embedding, and question-answering powered by ChromaDB and OpenAI-compatible LLMs.

![System Diagram](docs/system_flow.png) *(Example: Add your architecture diagram here)*

## Features

- **Multi-format Support**: Process Markdown, PDF, Word (.doc/.docx)
- **Smart Chunking**: Configurable text splitting with overlap
- **Semantic Search**: HNSW-powered vector similarity (ChromaDB)
- **LLM Integration**: Streaming responses with citation tracking
- **Production Ready**:
  - Environment variable configuration
  - Structured logging (file + stdout)
  - Type hints & PEP8 compliance
  - PyInstaller executable support

## Quick Start

```bash
# 1. Clone repo
git clone https://github.com/yourusername/document-qa-system.git
cd document-qa-system

# 2. Set up environment (Linux/macOS)
make install-dev
cp .env.example .env  # Edit with your API keys

# 3. Add documents to ./documents/
# 4. Run!
make run
```

## Configuration
Edit .env file
```bash
# Document Processing
CHUNK_SIZE=512      # Token size per chunk
CHUNK_OVERLAP=50    # Context overlap between chunks

# Vector DB
EMBEDDING_MODEL=all-MiniLM-L6-v2  # Sentence Transformer model

# LLM (OpenAI-compatible)
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

## Usage
1. Place documents in ./documents/
1. Launch the interactive Q&A interface:
```bash
make run
```
1. Enter questions when prompted:
```bash
Enter your question: What's the capital of France?
```
