import requests
import base64
import chardet
import json
import logging
import re
import os

# Configure logging
logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s -  %(message)s",
    level=logging.INFO
)

# Summary class to keep track of data about repo processing
class Summary:
    def __init__(self):
        self.repo_summary = {
            "total_files": 0,
            "processed_files": 0,
            "skipped_files": 0,
            "skipped_reasons": []
        }

        self.directory_structure = {}

        self.files = {}

    def process_file(self, path, status, content):

        self.files[f"Path: {path}"] = {
            "status": status,
            "content": content
        }
        
        self.repo_summary["total_files"] += 1
        if status == "processed":
            self.repo_summary["processed_files"] += 1
        elif status == "skipped":
            self.repo_summary["skipped_files"] +=1
            self.repo_summary["skipped_reasons"].append(content)

    def add_directory(self, directory_name, files_or_subdirs):
        self.directory_structure[directory_name] = files_or_subdirs

    def get_repo_summary(self):
        return self.repo_summary
        
    def get_directory_structure(self):
        return self.directory_structure
        
    def get_files(self):
        return self.files
        
    def print_summary(self, branch):

        data = {
        "Repo Summary": self.get_repo_summary(),
        "Branch": branch,
        "Directory Structure": self.get_directory_structure(),
        "Files": self.get_files()
        }

        return data



        

def parse_url(repo_url):
    return repo_url.rstrip('/').split('/')[-2:]

def check_response_code(response, repo_name, token=None):
    # check response code and respond accordingly
    # 401 (unauthorized) or 403 (Forbidden)
    if response.status_code in [401, 403]:
        if not token:
            # if no token was given, ask for one
            logging.error(f"Error: Repository '{repo_name}' is private. Authentication token required.")
            return False
        else:
            # if invalid token was given, ask for a new one
            logging.error(f"Error: Invalid token or permission issue for '{repo_name}'.")
            return False
    elif response.status_code != 200:
        logging.error(f"Error {response.status_code}: {response.text}")
        return False
    else:
        return True

def fetch_file_content(summary, owner, repo_name, file_path, branch="main", token=None):
    # Fetch the content of a file in the GitHub repo
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}?ref={branch}"

    # try to fetch with token if given, without if it isn't
    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(api_url, headers=headers)


    # end function if request is unsuccessful
    if not check_response_code(response, repo_name, token):
        summary.process_file( 
            (f'{repo_name}/{file_path}'), 
            'skipped',
            (f"Error {response.status_code}: {response.text}")
            )
        return None
    
    file_data = response.json()
    # get file content
    content = base64.b64decode(file_data['content'])

    # decect encoding
    detected_encoding = chardet.detect(content)['encoding']

    if detected_encoding in ['utf-8', 'ascii']:
        # decode the content only if it's utf-8
        try:
            decoded_content = content.decode('utf-8')
            
            summary.process_file(
                (f"{repo_name}/{file_path}"),
                'processed',
                (f"{decoded_content}")
            )
            return None
        except UnicodeDecodeError:
            summary.process_file(
                (f"{repo_name}/{file_path}"),
                'skipped',
                (f"Error decoding {file_path}: Content isn't valid UTF-8")
            )
            return None
    else:
        summary.process_file(
            (f"{repo_name}/{file_path}"),
            'skipped',
            (f"Skipping {file_path}: Detected encoding is {detected_encoding}")
        )
        return None

def fetch_repo_content(summary, repo_url, branch="main", token=None):
    # Extract repo owner and name from URL (user/repo-name)
    repo_parts = parse_url(repo_url)
    owner, repo_name = repo_parts[0], repo_parts[1]

    return process_directory(summary, owner, repo_name, '', branch, token)


def process_directory(summary, owner, repo_name, directory_path, branch="main", token=None):

    # GitHub API endpoint to fetch the repository contents
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents{directory_path}?ref={branch}"
    response = requests.get(api_url, token)

    # end function if request is unsuccessful
    if not check_response_code(response, repo_name, token):
        summary.process_file( 
            (f'{repo_name}/{directory_path}'), 
            'skipped',
            (f"Error {response.status_code}: {response.text}")
            )
        return None

    contents = response.json()
    directory_data = {}

    for item in contents:
        if item['type'] == 'file':
            fetch_file_content(summary, owner, repo_name, item['path'], branch, token)
        elif item['type'] == 'dir':
            process_directory(summary, owner, repo_name, item['path'], branch, token)
        directory_data[item['path']] = item['type']
    return None


def main():

    repo_url = os.getenv("GITHUB_REPO") or input("Enter the Github repo url: ")
    branch = input("Enter the branch name (default is 'main'): ").strip() or "main"
    token = os.getenv("GITHUB_TOKEN") or input("Enter the GitHub authentication token (optional, press Enter to skip): ")

    summary = Summary()

    fetch_repo_content(summary, repo_url, branch, token.strip() if token else None)

    safe_branch = re.sub(r'[\/:*?"<>|]', '_', branch)
    output_file_path = f"repo_output_{safe_branch}.json"

    data = summary.print_summary(branch)

    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=True)

if __name__ == "__main__":
    main()