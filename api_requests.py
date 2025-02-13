import requests
import time
import utils


class GithubAPI:
    def __init__(self, repo_url, logger, token=None, branch="main"):
        self.repo_owner, self.repo_name = utils.parse_url(repo_url)
        self.repo_url = repo_url
        self.token = token
        self.branch = branch
        self.logger = logger
        self.headers = {"Authorization": f"token {token}"} if token else {}

    def fetch_repo_content(self, summary):
        self.logger.info(f"Fetching repo content from {self.repo_url}")

        start_time = time.time()
        self.process_directory(summary, '')
        elapsed_time = time.time() - start_time

        self.logger.info(f"Content processed in {elapsed_time: 2f} seconds")
        self.logger.info(f"Total files processed: {summary.repo_summary['processed_files']}")
        self.logger.info(f"Total files skipped: {summary.repo_summary['skipped_files']}")

    
    def process_directory(self, summary, directory_path):
        self.logger.info(f"Processing directory: {directory_path if directory_path else 'root'} from {self.repo_url}")

        # GitHub API endpoint to fetch the repo contents
        api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{directory_path}?ref={self.branch}"
        response = requests.get(api_url, headers=self.headers)

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
        self.logger.info(f"Fetching file content: {file_path}")
        api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}?ref={self.branch}"
        response = requests.get(api_url, headers=self.headers)

        if not self.check_response_code(response):
            self.logger.error(f"Failed to fetch {file_path}: {response.status_code} - {response.text}")
            summary.process_file(
                (f"{self.repo_name}/{file_path}"),
                'skipped',
                (f"Error {response.status_code}: {response.text}")
            )
            return None
        
        file_data = response.json()

        if utils.is_config_file(file_path):
            self.logger.info(f"Summarizing config file: {file_path}")
            status, content = utils.summarize_config(file_data, file_path)
            
        else:
            self.logger.info(f"Decoding file: {file_path}")
            status, content = utils.decode_file_content(file_data)
        summary.process_file(
            (f"{self.repo_name}/{file_path}"),
            status, content
        )
        return

    def check_response_code(self, response):
        # check response code and respond accordingly
        if response.status_code == 200:
            return True
        elif response.status_code == 403:
            self.logger.warning("GitHub API rate limit exceeded or missing permissions.")
        elif response.status_code == 404:
            self.logger.warning(f"Resource not found: {response.url}")
        else:
            self.logger.error(f"API request failed: {response.status_code} - {response.text}")
        return False
    

