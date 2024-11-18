run-db:
	docker compose up -d


dev:
	uvicorn main:app --reload
