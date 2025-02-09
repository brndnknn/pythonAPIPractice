# Define variables
PYTHON = python 
SCRIPT = githubAPI.py
OUTPUT = repo_output_*.json
LOGS = *.log


# Default run command
run:
	@echo "Running script..."
	GITHUB_REPO="your-url-here" \
	GITHUB_TOKEN="your-token-here" \
	$(PYTHON) $(SCRIPT)

# clean up log and json files
clean:
	@echo "Cleaning up JSON and log files..."
	rm -f $(OUTPUT) $(LOGS)