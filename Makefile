db-up:
	docker compose up -d

db-migrate:
	poetry run alembic upgrade head

db-seed:
	poetry run python seed.py
	

dev-naive:
	uvicorn app:app --reload

dev:
	uvicorn main:app --reload
