# Load .env file if it exists
ifneq (,$(wildcard .env))
	include .env
	export
endif

# Define variables
PYTHON = python 
SCRIPT = main.py



# Default run command
run:
	@echo "Running script for active branches..."
	@branches="main $(shell git branch -r --no-merged origin/main | sed 's/origin\///')";\
	for branch in $$branches; do \
		echo "Running script for branch: $$branch"; \
		GITHUB_REPO="https://github.com/brndnknn/pythonAPIPractice" \
		$(PYTHON) $(SCRIPT) $$branch; \
	done


# Run for a specific GitHub repository (only main branch)
run-repo:
	@if [ -z "$(repo)" ]; then \
		echo "Usage: make run-repo repo=<username/repo>"; \
		exit 1; \
	fi; \
	echo "Fetching repo: $(repo) on main branch"; \
	GITHUB_REPO="https://github.com/$(repo)" \
	$(PYTHON) $(SCRIPT) main;



# Run for a spcific branch entered by the user
run-branch:
	@read -p "Enter branch name: " branch; \
	echo "Running script for branch: $$branch"; \
		GITHUB_REPO="https://github.com/brndnknn/pythonAPIPractice" \
		$(PYTHON) $(SCRIPT) $$branch; \

# clean up
clean:
	@echo "Cleaning up cache files..."
	rm -rf __pycache__/

deep-clean:
	@echo "Cleaning all script generated files..."
	rm -rf __pycache__ logs/ output/
