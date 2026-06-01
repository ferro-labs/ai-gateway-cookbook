# Recipe Makefile — copy-paste this into every new recipe.
# The only thing usually customised per recipe is IMAGE.

IMAGE ?= ferro-cookbook/_template:latest

.PHONY: help run test build clean

help:
	@echo "Targets:"
	@echo "  make build   - Build the recipe's Docker image"
	@echo "  make run     - Build + run the recipe (loads ./.env)"
	@echo "  make test    - Build + run mocked smoke tests"
	@echo "  make clean   - Remove the recipe's Docker image"

build:
	docker build -t $(IMAGE) .

run: build
	@test -f .env || (echo "ERROR: .env not found. Run 'cp .env.example .env' first."; exit 1)
	docker run --rm --env-file .env --network=host $(IMAGE)

test: build
	docker run --rm $(IMAGE) python -m py_compile recipe.py

clean:
	-docker rmi $(IMAGE)
