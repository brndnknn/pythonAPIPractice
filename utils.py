import base64
import chardet
import json
import xml.etree.ElementTree as ET
import yaml
import configparser

# Utility functions

def parse_url(repo_url):
    return repo_url.rstrip('/').split('/')[-2:]


# returns status, content
def decode_file_content(file_data):
    """Decodes Base64-encoded file content"""
    try:
        # get file content
        raw_content = base64.b64decode(file_data['content'])

        # detect encoding
        detected_encoding = chardet.detect(raw_content)['encoding']

        # Try to decode using detected encoding
        if detected_encoding:
            return "processed", raw_content.decode(detected_encoding, errors="replace")
        else:
            return "skipped", f"Error: Unknown encoding for {file_data.get('path', 'unknown file')}"

    except Exception as e:
        return "skipped", f"Error decoding file: {str(e)}"

def is_config_file(file_path):
    """Checks if a file is a config file based on filename or extension."""
    config_filenames = {
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml",  # NPM package managers
        "pom.xml", "build.gradle", "build.gradle.kts",  # Java build tools
        ".eslintrc.json", ".prettierrc", "tsconfig.json",  # JavaScript/TypeScript tools
        "pyproject.toml", "tox.ini", "setup.cfg",  # Python package configs
        "docker-compose.yml", "Dockerfile",  # Docker configs
        ".github/workflows", ".gitlab-ci.yml"  # CI/CD configs
    }
    
    # config_extensions = {".json", ".xml", ".yaml", ".yml", ".ini", ".toml"}

    filename = file_path.split("/")[-1].lower()

    # Check if filename is in the known config list or has a config extension
    return filename in config_filenames 
    
    # or any(filename.endswith(ext) for ext in config_extensions)



def summarize_config(file_data, file_path):
    summary = {
        "config-type": "unknown",
        "key-settings": {}
    }

    # Decode file content
    status, raw_content = decode_file_content(file_data)

    if status == "skipped":
        return status, raw_content
    
    try:
        # Process based on file extension
        if file_path.endswith(".json"):
            data = json.loads(raw_content)
            
            # Special case: package-lock.json
            if "lockfileVersion" in data:
                summary["config-type"] = "npm"
                summary["key-settings"]["lockfile-version"] = data.get("lockfileVersion")
                summary["key-settings"]["package-manager"] = "npm"

                # Extract dependencies (only top-level)
                direct_deps = data.get("packages", {}).get("", {}).get("dependencies", {})
                direct_dev_deps = data.get("packages", {}).get("", {}).get("devDependencies", {})

                summary["major-dependencies"] = direct_deps
                summary["dev-dependencies"] = direct_dev_deps
            
            else:
                summary["config-type"] = "json"
                summary["key-settings"] = {k: v for k, v in data.items() if isinstance(v, (str, int, bool))}
        
        elif file_path.endswith(".xml"):
            root = ET.fromstring(raw_content)
            summary["config-type"] = "xml"
            summary["key-settings"]["root-tag"] = root.tag
        
        elif file_path.endswith((".yaml", ".yml")):
            data = yaml.safe_load(raw_content)
            summary["config-type"] = "yaml"
            summary["key-settings"] = {k: v for k, v in data.items() if isinstance(v, (str, int, bool))}
        
        elif file_path.endswith((".ini", ".properties")):
            config = configparser.ConfigParser()
            config.read_string(raw_content)
            summary["config-type"] = "ini"
            summary["key-settings"] = {section: dict(config[section]) for section in config.sections()}
    
    except Exception as e:
        summary["warnings"].append(f"Error processing file: {str(e)}")
    
    return status, summary
