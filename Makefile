.PHONY: build
.SILENT:

args := $(wordlist 2, 100, $(MAKECMDGOALS))

env:
	cp .env.example .env

run:
	poetry run python3 -m app

revision: 
	cd app/db; poetry run alembic revision --autogenerate

upgrade:
	cd app/db; poetry run alembic upgrade $(args)

cache db:
	docker compose up -d --remove-orphans $@

build:
	docker build . -t project -f build/service/Dockerfile

up:
	docker compose up -d --remove-orphans

down:
	docker compose down
