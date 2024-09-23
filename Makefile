.PHONY: build up down attach bootstrap bash shell migrate migrations
build:
	docker compose build

up:
	make build
	docker compose up

down:
	docker compose down


attach:
	docker attach django_app

bootstrap:
	docker exec -it django_app python manage.py migrate
	docker exec -it django_app python manage.py loaddata sis_exercise/fixtures/literature.json
	docker exec -it django_app python manage.py loaddata sis_exercise/fixtures/users.json
	docker exec -it django_app python manage.py search_index --rebuild -f

bash:
	docker exec -it django_app bash

shell:
	docker exec -it django_app python manage.py shell

migrate:
	docker exec -it django_app python manage.py migrate

migrations:
	docker exec -it django_app python manage.py makemigrations

search-index-rebuild:
	docker exec -it django_app python manage.py search_index --rebuild
