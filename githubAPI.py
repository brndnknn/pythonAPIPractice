import requests
import json
import logging
import re
import os
import sys
from summary import Summary
from api_requests import GithubAPI
from utils import parse_url
from utils import decode_file_content


# Configure logging
logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s -  %(message)s",
    level=logging.INFO
)

def main():

    repo_url = os.getenv("GITHUB_REPO") or input("Enter the Github repo url: ")

    # If a branch is passed as an argument, use it
    if len(sys.argv) > 1:
        branch = sys.argv[1]
    else:
        branch = input("Enter the branch name (default is 'main'): ").strip() or "main"

    token = os.getenv("GITHUB_TOKEN") or input("Enter the GitHub authentication token (optional, press Enter to skip): ")

    

    github_api = GithubAPI(repo_url, token, branch)
    summary = Summary()

    github_api.fetch_repo_content(summary)

    safe_branch = re.sub(r'[\/:*?"<>|]', '_', branch)
    output_file_path = f"repo_output_{safe_branch}.json"

    data = summary.print_summary(branch)

    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=True)

if __name__ == "__main__":
    main()