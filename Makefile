CURRENT_DIRECTORY := $(shell pwd)

TESTSCOPE = apps
TESTFLAGS = --with-timer --timer-top-n 10 --keepdb

help:
	@echo "Docker Compose Help"
	@echo "-----------------------"
	@echo ""
	@echo "Run tests to ensure current state is good:"
	@echo "    make test"
	@echo ""
	@echo "If tests pass, add fixture data and start up the api:"
	@echo "    make begin"
	@echo ""
	@echo "Really, really start over:"
	@echo "    make clean"
	@echo ""
	@echo "See contents of Makefile for more targets."

begin: migrate fixtures start

start:
	@docker-compose up

start_db:
	@docker-compose up l8ser-db

stop:
	@docker-compose stop

down:
	@docker-compose down

status:
	@docker-compose ps

restart: stop start

clean: stop
	@docker-compose down -v
	@docker-compose rm --force
	@find . -name \*.pyc -delete

build:
	@docker-compose build l8ser-api

test:
	@docker-compose exec l8ser-api python ./manage.py test ${TESTSCOPE} ${TESTFLAGS}

makemigrations:
	@docker-compose exec l8ser-api python ./manage.py makemigrations

migrate:
	@docker-compose exec l8ser-api python ./manage.py migrate

cli:
	@docker-compose exec l8ser-api bash

tail:
	@docker-compose logs -f

createsuperuser:
	@docker-compose exec l8ser-api python ./manage.py createsuperuser

startapp:
	@docker-compose exec l8ser-api python ./manage.py startapp ${APP_NAME}

.PHONY: start stop status restart clean build test migrate cli tail createsuperuser
