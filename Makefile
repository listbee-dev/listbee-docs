.PHONY: preview build deploy sync

sync:
	curl -sf https://api.listbee.so/openapi.json > fern/openapi/openapi.json
	python scripts/generate_overrides.py

preview:
	npx fern docs dev

build:
	npx fern generate --docs

deploy: sync
	npx fern generate --docs --force
