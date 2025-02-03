import requests
import base64
import chardet

def parse_url(repo_url):
    return repo_url.rstrip('/').split('/')[-2:]

def check_response_code(response, repo_name, token):
    # check response code and respond accordingly
    # 401 (unauthorized) or 403 (Forbidden)
    if response.status_code in [401, 403]:
        if not token:
            # if no token was given, ask for one
            print(f"Error: Repository '{repo_name}' is private. Authentication token required.")
            return False
        else:
            # if invalid token was given, ask for a new one
            print(f"Error: Invalid token or permission issue for '{repo_name}'.")
            return False
    elif response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return False
    else:
        return True

def fetch_file_content(owner, repo_name, file_path, token=None):
    # Fetch the content of a file in the GitHub repo
    api_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}'

    # try to fetch with token if given, without if it isn't
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    response = requests.get(api_url, headers=headers)


    # end function if request is unsuccessful
    if not check_response_code(response, repo_name, token):
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
            return decoded_content
        except UnicodeDecodeError:
            print(f"Error decoding {file_path}: Content isn't valid UTF-8")
            return None
    else:
        print(f"Skipping {file_path}: Detected encoding is {detected_encoding}")
        return None

def fetch_repo_content(repo_url, token=None):
    # Extract repo owner and name from URL (user/repo-name)
    repo_parts = parse_url(repo_url)
    owner, repo_name = repo_parts[0], repo_parts[1]

    return process_directory(owner, repo_name, '', token)


def process_directory(owner, repo_name, directory_path, token=None):

    # GitHub API endpoint to fetch the repository contents
    api_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents{directory_path}'
    response = requests.get(api_url)

    # end function if request is unsuccessful
    if not check_response_code(response, repo_name, token):
        return None

    contents = response.json()
    repo_data = {}

    for item in contents:
        if item['type'] == 'file':
            file_content = fetch_file_content(owner, repo_name, item['path'])
            if file_content:
                repo_data[item['path']] = file_content
        elif item['type'] == 'dir':
            # Recursively process subdirectories
            repo_data[item['path']] = process_directory(owner, repo_name, item['path'])

    return repo_data




repo_url = 'https://github.com/brndnknn/project-pixel'
repo_content = fetch_repo_content(repo_url)
print(repo_content)