COMPOSE = docker compose

.PHONY: up down build logs shell migrate makemigrations createsuperuser check compilemessages

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f web

shell:
	$(COMPOSE) exec web sh

migrate:
	$(COMPOSE) exec web python manage.py migrate

makemigrations:
	$(COMPOSE) exec web python manage.py makemigrations

createsuperuser:
	$(COMPOSE) exec web python manage.py createsuperuser

check:
	$(COMPOSE) exec web python manage.py check

compilemessages:
	$(COMPOSE) exec web python manage.py compilemessages

