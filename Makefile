update:
	docker-compose build web

migrate:
	docker-compose run web python manage.py migrate

collectstatic:
	docker-compose run web python manage.py collectstatic --noinput

run:
	docker-compose up -d

stop:
	docker-compose down