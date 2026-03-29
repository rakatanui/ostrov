COMPOSE = docker compose
export ENV_VARS_FILE ?= .env.production
export JOB_NAME_PREFIX ?= ostrov-quest

.PHONY: up down build logs shell migrate makemigrations createsuperuser check compilemessages cloud-build cloud-deploy cloud-migrate cloud-collectstatic cloud-check cloud-superuser

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

cloud-build:
	bash scripts/cloudrun/build-image.sh

cloud-deploy:
	bash scripts/cloudrun/deploy-service.sh

cloud-migrate:
	bash scripts/cloudrun/run-job.sh $(JOB_NAME_PREFIX)-migrate python manage.py migrate --noinput

cloud-collectstatic:
	bash scripts/cloudrun/run-job.sh $(JOB_NAME_PREFIX)-collectstatic python manage.py collectstatic --noinput

cloud-check:
	bash scripts/cloudrun/run-job.sh $(JOB_NAME_PREFIX)-check python manage.py check --deploy

cloud-superuser:
	bash scripts/cloudrun/run-job.sh $(JOB_NAME_PREFIX)-superuser python manage.py ensure_superuser --skip-if-missing
