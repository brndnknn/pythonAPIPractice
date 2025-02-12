import requests
# from summary import Summary
from utils import parse_url
from utils import decode_file_content


class GithubAPI:
    def __init__(self, repo_url, token=None, branch="main"):
        self.repo_owner, self.repo_name = parse_url(repo_url)
        self.token = token
        self.branch = branch
        self.headers = {"Authorization": f"token {token}"} if token else {}

    def fetch_repo_content(self, summary):

        return self.process_directory(summary, '')
    
    def process_directory(self, summary, directory_path):
        # GitHub API endpoint to fetch the repo contents
        api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{directory_path}?ref={self.branch}"
        response = requests.get(api_url, self.headers)

        if not self.check_response_code(response):
            summary.process_file(
                (f"{self.repo_name}/{directory_path}"),
                'skipped',
                (f"Error {response.status_code}: {response.text}")
            )
            return None
        
        contents = response.json()

        for item in contents:
            if item['type'] == 'file':
                self.fetch_file_content(summary, item['path'])
            elif item['type'] == 'dir':
                self.process_directory(summary, item['path'])
            # what happens if neither file nor dir? is that possible? 


    def fetch_file_content(self, summary, file_path):
        # fetch the content of a file in the GitHub repo
        api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}?ref={self.branch}"
        response = requests.get(api_url, self.headers)

        if not self.check_response_code(response):
            summary.process_file(
                (f"{self.repo_name}/{file_path}"),
                'skipped',
                (f"Error {response.status_code}: {response.text}")
            )
            return None
        
        file_data = response.json()

        status, content = decode_file_content(file_data)
        summary.process_file(
            (f"{self.repo_name}/{file_path}"),
            status, content
        )
        return

    def check_response_code(self, response):
        # check response code and respond accordingly
        if response.status_code == 200:
            return True
        else:
            return False
    

