COMPOSE = docker compose
SERVICE = web


up:
	$(COMPOSE) up

up-watch:
	$(COMPOSE) up --watch

up-build:
	$(COMPOSE) up --build

build:
	$(COMPOSE) build --no-cache

up-d:
	$(COMPOSE) up -d

enter:
	$(COMPOSE) exec $(SERVICE) bash

createsuperuser:
	$(COMPOSE) exec $(SERVICE) python manage.py createsuperuser

down:
	$(COMPOSE) down

migrate:
	$(COMPOSE) exec $(SERVICE) python manage.py migrate

dbbackup:
	$(COMPOSE) exec $(SERVICE) python manage.py dbbackup


migrations:
	$(COMPOSE) exec $(SERVICE) python manage.py makemigrations

showmigrations:
	$(COMPOSE) exec $(SERVICE) python manage.py showmigrations


load_books:
	$(COMPOSE) exec $(SERVICE) python manage.py load_books