import os
from yaspin import yaspin
import requests
from file_processing.error_handling import Failure, Ok


def process_file(file_path):
    """Reads the content of a file and returns it as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Store file content in a string
            return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


async def createRemoteFile(url: str, folderID: str, filePath: str, fileContent: str):
    try:
        doc = {
                "fileContent": content,
                "folderID": folderID,
                "filePath": filePath,
                "fileContent": fileContent
            }
        await requests.post(url, json=doc)
    except Exception as error:
        failure = Failure(error)
        return failure


@yaspin(text="Scanning project...")
def process_directory(directory, url: str, folderID: str)-> str:
    loader = yaspin()
    loader.start()
    """Walks through the directory and reads each file's content into a string."""
    
    # Walk through the directory and its subdirectories
    folders_to_ignore = ".pytest_cache __pycache__ node_modules dist ano_code.egg-info auto-code-env"
    process_file(".gitignore")

    fl = {".py", ".js", ".go", ".ts", ".tsx", ".jsx", ".dart", ".php", "Dockerfile", "docker-compose.yml"}
    
    
    code = ""
    for root, dirs, files in os.walk(directory):
        if ".gitignore" in files:
            ign_file_idx = files.index(".gitignore")
            if type(ign_file_idx) == int:
                res = process_file(files[ign_file_idx])
                if type(res) == str:
                    folders_to_ignore += f" ${res}"
        
        
        # Modify dirs in-place to exclude specific directories
        dirs[:] = [d for d in dirs if d not in folders_to_ignore]
        for filename in files:
        # Check if the file has an excluded extension
            if filename.endswith(tuple(fl)):
                file_path = os.path.join(root, filename)
                content = process_file(file_path)  # Read file into a string
                
                if content is not None:
                    if filename:
                        code += f"{content}\n"
                        createRemoteFile(url, folderID, file_path, content)

    loader.stop()
    return code

