.PHONY: build up down logs test

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	curl -X POST http://localhost:8001/webhook \
	  -H "Content-Type: application/json" \
	  -H "X-Event-Type: test" \
	  -H "X-Signature-256: sha256=24c848fb62413346eccfed66a01ba14c538fd1220613e9e3ecb7b4fec6bdc071" \
	  -d '{"message": "hello from webhook!"}'
