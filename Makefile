NAME=a_maze_ing.py

build-mazegen:
	@echo "\033[1;34mBuilding mazegen package...\033[0m"
	cd mazegen && poetry build -o ../dist \

install: build-mazegen
	@echo "\033[1;34mInstalling dependencies...\033[0m"
	@poetry install
	@echo "\n\033[1;32m✓ Done!\033[0m"
	@echo "\n\033[1;33mTo activate the virtual environment, run:\033[0m"
	@echo "\033[1;36m  source $(shell poetry env activate)\033[0m\n"

run:
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "Correct: VIRTUAL_ENV is set. Running program."; \
		python3 ./src/$(NAME); \
	else \
		echo "Error: VIRTUAL_ENV is not set. Please activate your virtual environment first."; \
		echo "`make install` or `poetry activate`"; \
		echo "make install."; \
		exit 1; \
	fi

lint:
	@echo "🔍 Running linters..."
	python3 -m mypy .
	python3 -m flake8 .
	@echo "✓ Linting complete."
	

lint-strict: lint
	@echo "🔒 Running strict linters..."
	python3 -m flake8 .
	python3 -m mypy . --strict
	@echo "✓ Strict linting complete."

clean:
	@echo "🧹 Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "poetry.lock" -delete
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	@find . -type d -name "dist" -prune -exec rm -rf {} +
	@find . -type d -name "build" -prune -exec rm -rf {} +
	@echo "✓ Clean complete."

deactivate:
	poetry env remove --all

.SILENT: install lint lint-strict
.PHONY: install run clean lint lint-strict
