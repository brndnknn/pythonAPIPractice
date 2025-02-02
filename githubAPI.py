import requests

def fetch_repo_content(repo_url):
    # Extract repo owner and name from URL (user/repo-name)
    repo_parts = repo_url.rstrip('/').split('/')[-2:]
    owner, repo_name = repo_parts[0], repo_parts[1]

    # GitHub API endpoint to fetch the repository contents
    api_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents'
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
repo_url = 'https://github.com/brndnknn/project-pixel'
repo_content = fetch_repo_content(repo_url)
print(repo_content)