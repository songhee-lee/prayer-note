.PHONY: help install run test migrate upgrade downgrade clean docker-up docker-down

help:
	@echo "Prayer Note Backend - Available Commands"
	@echo "========================================"
	@echo "install       - Install dependencies"
	@echo "run           - Run development server"
	@echo "test          - Run tests"
	@echo "migrate       - Create new migration"
	@echo "upgrade       - Apply migrations"
	@echo "downgrade     - Rollback last migration"
	@echo "clean         - Clean cache and temporary files"
	@echo "docker-up     - Start Docker containers"
	@echo "docker-down   - Stop Docker containers"
	@echo "format        - Format code with black"
	@echo "lint          - Lint code with flake8"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

migrate:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

format:
	black app/ tests/

lint:
	flake8 app/ tests/
