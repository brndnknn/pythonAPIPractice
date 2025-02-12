import base64
import chardet

# Utility functions

def parse_url(repo_url):
    return repo_url.rstrip('/').split('/')[-2:]


# returns status, content
def decode_file_content(file_data):
    # get file content
    content = base64.b64decode(file_data['content'])

    # detect encoding
    detected_encoding = chardet.detect(content)['encoding']

    if detected_encoding in ['utf-8', 'ascii']:
        # decode only if it's utf-8
        try:
            decoded_content = content.decode('utf-8')

            return ('processed', f"{decoded_content}")
        except UnicodeDecodeError:
            
            return('skipped', (f"Error decoding {file_data.path}: Content isn't valid UTF-8"))
        
    else:
        return ('skipped', (f"Skipping {file_data.path}: Detected encoding is {detected_encoding}"))


