# GitHub API JSON Generator for GPT

## Overview
This Python script interacts with the GitHub API to retrieve repository contents and generate structured JSON output. The primary purpose of this script is to create JSON data that can be fed into a GPT model for analysis, processing, or further automation. 

### Why Use This Tool?
- Easily fetch and analyze GitHub repository structures.
- Automate repository content extraction for AI/ML applications.
- Simplify JSON generation for code review and documentation.

## Features
- Fetch repository file contents using the GitHub API.
- Handle authentication for private repositories.
- Detect and decode file encodings (UTF-8, ASCII).
- Generate a structured JSON file containing:
  - Repository summary.
  - Directory structure.
  - Processed file contents.
- Specify a subdirectory to limit processing to only relevant files.

## Directory Structure
```
pythonAPIPractice/
├── .gitignore          # Ignore unnecessary files
├── Makefile            # Run and cleanup commands
├── README.md           # Project documentation
├── api_requests.py     # Handles API requests to GitHub
├── logger.py           # Logging utility for tracking script execution
├── main.py             # Entry point of the script
├── summary.py          # Summarizes processed files and repository structure
├── utils.py            # Helper functions for encoding, parsing, and file processing
├── output/             # Directory for script-generated files
│   ├── repo_output.json  # JSON output formatted for GPT input
├── logs/               # Stores log files
```

## Installation
1. **Clone this repository:**
   ```sh
   git clone https://github.com/your-username/your-repo.git
   cd your-repo/pythonAPIPractice
   ```
2. **Install required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up GitHub authentication (if needed for private repos):**
   ```sh
   export GITHUB_TOKEN=your_personal_access_token
   ```

## Usage
### Running the script
Run the script and provide the GitHub repository URL when prompted:
```sh
python githubAPI.py
```
Alternatively, you can specify a repository directly using `make`:
```sh
make run repo=username/repository
```
To run for a specific branch:
```sh
make run-branch repo=username/repository
```
### Fetching Only a Specific Subdirectory

If you only want to process a subdirectory of a repository (e.g., just the frontend/ folder), specify it in the URL:

**Option 1: Full GitHub URL Format**
```sh
https://github.com/user/repo/tree/main/frontend
```
**Option 2: Shorthand Format**
```sh
user/repo/frontend
```

The script will detect the subdirectory and treat it as the root directory for processing.


## Output
The script generates a `repo_output.json` file containing:
- A summary of processed files.
- The repository's directory structure.
- File contents (if accessible).

### Example JSON Output
```json
{
  "Repo Summary": {
    "total_files": 8,
    "processed_files": 8,
    "skipped_files": 0
  },
  "Branch": "main",
  "Directory Structure": {},
  "Files": {
    "Path: pythonAPIPractice/githubAPI.py": {
      "status": "processed",
      "content": "import requests..."
    }
  }
}
```

### Using the JSON Output with GPT
The `repo_output.json` file is specifically designed to be used as input for a GPT model. You can provide this JSON to a GPT-based tool to analyze the repository, generate documentation, suggest improvements, or assist with code review.

## License
This project is licensed under the MIT License.

