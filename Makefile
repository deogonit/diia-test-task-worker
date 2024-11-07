start-cron:
	docker-compose --profile cron up -d

stop-cron:
	docker-compose --profile cron down

start-script:
	docker-compose --profile script-only up -d

stop-script:
	docker-compose --profile script-only down

run:
	python src/main.py

lint:
	ruff check src/

format:
	ruff format src/
