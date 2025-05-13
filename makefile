up:
	docker compose up

build:
	docker compose build

down:
	docker compose down

lint:
	black core
	black --exclude migrations tickets
	isort --profile black core
	isort --profile black --skip migrations tickets
