COMPOSE ?= docker compose

.PHONY: help run test down clean logs

help:
	@echo "Targets:"
	@echo "  make run    - Start gateway + recipe via docker compose (loads ./.env)"
	@echo "  make test   - Run the mocked smoke test (no gateway, no provider calls)"
	@echo "  make down   - Stop and remove the compose stack"
	@echo "  make clean  - Stop the stack and remove its images"
	@echo "  make logs   - Tail the running stack logs"

run:
	@test -f .env || (echo "ERROR: .env not found. Run 'cp .env.example .env' first."; exit 1)
	$(COMPOSE) up --build --abort-on-container-exit --exit-code-from recipe

# Mocked smoke test: build only the recipe image and run unittest with the
# gateway dependency skipped (--no-deps) — no provider keys, no live calls.
test:
	$(COMPOSE) build recipe
	$(COMPOSE) run --rm --no-deps recipe python -m unittest -v test_agent.py

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) down --rmi local --remove-orphans

logs:
	$(COMPOSE) logs -f
