# GitHub API JSON Generator for GPT  

## Overview  
This Python script interacts with the GitHub API to retrieve repository contents and generate structured JSON output. The primary purpose of this script is to create JSON data that can be fed into a GPT model for analysis, processing, or further automation.  

## Features  
- Fetch repository file contents using the GitHub API  
- Handle authentication for private repositories  
- Detect and decode file encodings (UTF-8, ASCII)  
- Generate a structured JSON file containing:  
  - Repository summary  
  - Directory structure  
  - Processed file contents  

## Directory Structure  
```
pythonAPIPractice/
│── githubAPI.py  # Main script for fetching GitHub repository data  
│── repo_output.json  # JSON output formatted for GPT input  
```  

## Installation  
1. Clone this repository:  
   ```sh
   git clone https://github.com/your-username/your-repo.git  
   cd your-repo/pythonAPIPractice  
   ```  
2. Install required dependencies:  
   ```sh
   pip install requests chardet  
   ```  

## Usage  
Run the script and provide the GitHub repository URL when prompted:  
```sh
python githubAPI.py  
```  
You may also provide a GitHub authentication token for private repositories.  

## Output  
The script generates a `repo_output.json` file containing:  
- A summary of processed files  
- The repository's directory structure  
- File contents (if accessible)  

### **Using the JSON Output with GPT**  
The `repo_output.json` file is specifically designed to be used as input for a GPT model. You can provide this JSON to a GPT-based tool to analyze the repository, generate documentation, suggest improvements, or assist with code review.  

## License  
This project is licensed under the MIT License.  
