.PHONY: help upgrade downgrade revision current history


help:
	@echo "Available commands:"
	@echo "  make upgrade       - Apply all migrations (upgrade to head)"
	@echo "  make downgrade     - Rollback last migration"
	@echo "  make downgrade-base- Rollback all migrations (to base)"
	@echo "  make revision MSG=\"message\" - Create new migration with message"
	@echo "  make current       - Show current migration in database"
	@echo "  make history       - Show all migrations history"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

downgrade-base:
	alembic downgrade base

revision:
ifndef MSG
	$(error MSG is required. Usage: make revision MSG="your message")
endif
	alembic revision --autogenerate -m "$(MSG)"

current:
	alembic current

history:
	alembic history

test:
	pytest

req:
	poetry export -f requirements.txt --without-hashes --output requirements.txt
