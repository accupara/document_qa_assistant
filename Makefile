# Makefile for Document QA System

# Configuration
VENV_NAME?=dqavenv
PYTHON?=python3
PIP?=pip
TEST_DIR?=tests/
DOCS_DIR?=documents/
LOG_DIR?=logs/
CHROMA_DB_DIR?=chroma_db/
COLLECTION_NAME?=document_qa

# Targets
.PHONY: all install install-dev clean test lint format run build package help

all: install-dev

## Environment setup
venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
	test -d $(VENV_NAME) || $(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && $(PIP) install --upgrade pip
	. $(VENV_NAME)/bin/activate && $(PIP) install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

install: venv
	. $(VENV_NAME)/bin/activate && $(PIP) install -r requirements.txt

install-dev: venv
	. $(VENV_NAME)/bin/activate && $(PIP) install -r requirements.txt
	. $(VENV_NAME)/bin/activate && $(PIP) install pytest pytest-cov pylint black mypy

clean:
	rm -rf $(VENV_NAME)
	rm -rf $(LOG_DIR)
	rm -rf $(CHROMA_DB_DIR)
	rm -rf __pycache__
	rm -rf $(TEST_DIR)/__pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf build dist *.spec
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

## Testing
test: venv
	. $(VENV_NAME)/bin/activate && pytest -v --cov=core --cov-report=html $(TEST_DIR)

test-ci: venv
	. $(VENV_NAME)/bin/activate && pytest --cov=core --cov-report=xml $(TEST_DIR)

## Code quality
lint: venv
	. $(VENV_NAME)/bin/activate && pylint core/ tests/ main.py
	. $(VENV_NAME)/bin/activate && mypy core/ tests/ main.py

format: venv
	. $(VENV_NAME)/bin/activate && black core/ tests/ main.py

## Application
run: venv
	mkdir -p $(DOCS_DIR)
	mkdir -p $(LOG_DIR)
	mkdir -p $(CHROMA_DB_DIR)
	. $(VENV_NAME)/bin/activate && $(PYTHON) main.py

## Build and packaging
build: venv
	. $(VENV_NAME)/bin/activate && pyinstaller --onefile --name document_qa main.py

package: venv
	. $(VENV_NAME)/bin/activate && $(PYTHON) setup.py sdist bdist_wheel

## Help
help:
	@echo "Document QA System Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install       - install production dependencies"
	@echo "  make install-dev  - install development dependencies"
	@echo "  make clean        - remove all generated files"
	@echo "  make test         - run tests with coverage"
	@echo "  make test-ci      - run tests for CI with XML coverage"
	@echo "  make lint         - run pylint and mypy"
	@echo "  make format       - format code with black"
	@echo "  make run          - run the application"
	@echo "  make build        - build executable with PyInstaller"
	@echo "  make package      - build Python package"
	@echo "  make help         - show this help"