up:
	docker compose up

build:
	docker compose build

down:
	docker compose down

test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from app