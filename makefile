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

test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from app
