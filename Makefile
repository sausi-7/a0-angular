.PHONY: help install dev dev-api dev-web dev-docker down test lint fmt clean

SHELL := /bin/bash

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install api and web deps
	cd apps/api && uv sync --all-extras --dev
	cd apps/web && npm install

dev: ## Run api + web in parallel (Ctrl+C stops both)
	$(MAKE) -j2 dev-api dev-web

dev-api: ## Run just the FastAPI backend
	cd apps/api && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-web: ## Run just the Angular dev server
	cd apps/web && npm start

dev-docker: ## Optional: run full stack via docker compose
	docker compose up --build

down: ## Stop docker compose stack
	docker compose down

test: ## Run unit tests for api and web
	cd apps/api && uv run pytest -q
	cd apps/web && npm test -- --watch=false --browsers=ChromeHeadless

lint: ## Run linters and type checks
	cd apps/api && uv run ruff check . && uv run ruff format --check . && uv run mypy .
	cd apps/web && npm run lint && npx tsc --noEmit

fmt: ## Format code
	cd apps/api && uv run ruff format .
	cd apps/web && npm run format

clean: ## Remove build artifacts and caches
	rm -rf apps/api/.venv apps/api/.pytest_cache apps/api/.mypy_cache apps/api/.ruff_cache apps/api/dist
	rm -rf apps/web/node_modules apps/web/.angular apps/web/dist
