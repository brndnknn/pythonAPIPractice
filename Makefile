# Load .env file if it exists
ifneq (,$(wildcard .env))
	include .env
	export
endif

# Define variables
PYTHON = python 
SCRIPT = main.py



# Default run command
# Run for a specific GitHub repository (only main branch)
run:
	@if [ -z "$(repo)" ]; then \
		echo "Usage: make run-repo repo=<username/repo>"; \
		exit 1; \
	fi; \
	echo "Fetching repo: $(repo) on main branch"; \
	GITHUB_REPO="https://github.com/$(repo)" \
	$(PYTHON) $(SCRIPT) main;



# Run for a spcific branch entered by the user
run-branch:
	@if [ -z "$(repo)" ]; then \
		echo "Usage: make run-repo repo=<username/repo>"; \
		exit 1; \
	fi; \
	branch=$$(bash -c 'read -p "Enter branch name: " branch; echo $$branch'); \
	echo "Running script for branch: $$branch"; \
		GITHUB_REPO="https://github.com/$(repo)" \
		$(PYTHON) $(SCRIPT) $$branch; \

# clean up
clean:
	@echo "Cleaning up cache files..."
	rm -rf __pycache__/

deep-clean:
	@echo "Cleaning all script generated files..."
	rm -rf __pycache__ logs/ output/
