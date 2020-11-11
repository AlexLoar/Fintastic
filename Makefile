# Run Tests
test:
	docker-compose -f docker-compose-local.yml run --rm web python ./manage.py test -v 2 tests --settings=config.settings.test

# Pipenv
pipenv_install:
	docker-compose -f docker-compose-local.yml run --rm web pipenv install

# Django shell
shell:
	docker-compose -f docker-compose-local.yml run --rm web python ./manage.py shell

# Django migrate
migrate:
	docker-compose -f docker-compose-local.yml run --rm web python ./manage.py migrate

# Django makemigrations
makemigrations:
	docker-compose -f docker-compose-local.yml run --rm web python ./manage.py makemigrations

# Django create new app
start_app:
	docker-compose -f docker-compose-local.yml run --rm web python ./manage.py startapp $(app_name)

# Start container
up:
	docker-compose -f docker-compose-local.yml up

# Start container in background
upd:
	docker-compose -f docker-compose-local.yml up -d

# Stop container
down:
	docker-compose -f docker-compose-local.yml down

# Build container
build:
	docker-compose -f docker-compose-local.yml build
