.PHONY: sync-openapi preview build

sync-openapi:
	curl -s https://api.listbee.so/openapi.json > fern/openapi/openapi.json

sync-openapi-dev:
	curl -s http://localhost:8000/_api/openapi.json > fern/openapi/openapi.json

preview:
	npx fern docs dev

build:
	npx fern generate --docs

deploy:
	npx fern generate --docs
