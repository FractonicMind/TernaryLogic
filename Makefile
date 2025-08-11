# Ternary Logic Framework - Makefile
# Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)

help:
	@echo "Ternary Logic Framework - Available Commands"
	@echo "============================================"
	@echo "  make install    - Install all dependencies"
	@echo "  make test       - Run all 53 tests"
	@echo "  make quick      - Run tests quickly"
	@echo "  make coverage   - Run tests with coverage"
	@echo "  make clean      - Clean up files"
	@echo ""
	@echo "Created by Lev Goukassian"

install:
	pip install -e .
	pip install pytest pytest-cov pytest-mock

test:
	python -m pytest tests/ -v

quick:
	python -m pytest tests/ -q

coverage:
	python -m pytest tests/ --cov=src/goukassian --cov-report=term-missing

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage *.egg-info

.PHONY: help install test quick coverage clean
