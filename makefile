.PHONY := install, install-dev, help, tools, clean
.DEFAULT_GOAL := install-dev

INS=$(wildcard requirements*.in)
REQS=$(subst in,txt,$(INS))

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.%.in:
	@touch $@

requirements.%.txt: requirements.%.in
	@echo "Building $@"
	@pip-compile --no-emit-index-url -q -o $@ $^

requirements.in:
	touch $@

requirements.txt: requirements.in
	@echo "Building $@"
	@pip-compile --no-emit-index-url -q -o $@ $^

install: requirements.txt ## Install production requirements
	@pip -q install pip-tools
	@echo "Installing $^"
	@pip-sync $^

install-dev: $(REQS) ## Install development requirements (default)
	@pip -q install pip-tools
	@echo "Installing $^"
	@pip-sync $^

clean: ## Clean any tempory and build files
	@find . -type f -name '*.pyc' -exec rm -f {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@rm -rf *.egg-info
