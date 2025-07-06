


run:
	pip3 freeze > requirements.txt
	docker compose up --build -d

initialize_db:
	DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres" python app/models/database_initialize.py