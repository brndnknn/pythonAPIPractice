# Define variables
PYTHON = python 
SCRIPT = githubAPI.py
OUTPUT = repo_output_*.json
LOGS = *.log


# Default run command
run:
	@echo "Running script for active branches..."
	@branches="main $(shell git branch -r --no-merged origin/main | sed 's/origin\///')";\
	for branch in $$branches; do \
		echo "Running script for branch: $$branch"; \
		GITHUB_REPO="your-url-here" \
		GITHUB_TOKEN="your-token-here" \
		$(PYTHON) $(SCRIPT) $$branch; \
	done

# Run for a spcific branch entered by the user
run-branch:
	@read -p "Enter branch name: " branch; \
	echo "Running script for branch: $$branch"; \
		GITHUB_REPO="your-url-here" \
		GITHUB_TOKEN="your-token-here" \
		$(PYTHON) $(SCRIPT) $$branch; \

# clean up log and json files
clean:
	@echo "Cleaning up JSON and log files..."
	rm -f $(OUTPUT) $(LOGS)