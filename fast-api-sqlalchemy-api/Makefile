start:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

list:
	docker-compose ps

run:
	python main.py

create-tables:
	python create_tables.py

access-db:
	docker exec -it fast-api-sqlalchemy-api_db_1 psql -U postgres -d courses
