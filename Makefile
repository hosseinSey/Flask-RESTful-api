.PHONY: help
help: ## Print this help message and exit
	@echo Usage:
	@echo "  make [target]"
	@echo
	@echo Targets:
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "  %-30s %s\n", $$1, $$NF \
		 }' $(MAKEFILE_LIST)

.PHONY: build
build: ## Build the development docker container
	docker-compose \
		-f devstack/docker-compose.yaml \
		build

.PHONY: up
up: ## Run a local development server
	docker-compose \
		-f devstack/docker-compose.yaml \
		up

.PHONY: run
run: ## Run the bash command inside the docker
	docker-compose \
		-f devstack/docker-compose.yaml \
		run --service-ports udemiapi 

.PHONY: test-unit
test-unit: ## Run unit tests
	docker-compose \
		-f devstack/docker-compose.yaml \
		run activitysvc \
		pytest tests/

.PHONY: test-functional
test-functional: ## Run HTTP functional tests
	docker-compose \
		-f devstack/docker-compose.yaml \
		run activitysvc \
		pytest tests-functional/

.PHONY: test
test: ## Run all the tests -- units and HTTP functionals
	docker-compose \
		-f devstack/docker-compose.yaml \
		run activitysvc \
		pytest

.PHONY: coverage
coverage: ## Measure and report the coverage of unit tests
	docker-compose \
		-f devstack/docker-compose.yaml \
		run activitysvc \
		bash -c "coverage run /usr/local/bin/pytest  tests/ && coverage report -m"
