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