.PHONY: up down build seed logs shell-backend shell-db migrate

up:
	docker compose up --build -d

down:
	docker compose down

build:
	docker compose build

migrate:
	docker compose run --rm migrate

seed:
	docker compose run --rm seed

logs:
	docker compose logs -f backend

shell-backend:
	docker compose exec backend bash

shell-db:
	docker compose exec db mysql -u governance_user -pgovernance_pass governance_db

restart-backend:
	docker compose restart backend
