import os


def create_directory(folder_name):
    # Get current working directory
    current_dir = os.getcwd()
    # Join current directory with folder name
    dir = os.path.join(current_dir, folder_name)
    
    # Create folder if not exists
    os.makedirs(dir, exist_ok=True)
