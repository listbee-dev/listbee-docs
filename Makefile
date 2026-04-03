.PHONY: preview build deploy

preview:
	npx fern docs dev

build:
	npx fern generate --docs

deploy:
	npx fern generate --docs --force
