import os

def create_test_directory(test_id):
    current_dir = os.getcwd()  # Get current working directory
    test_dir = os.path.join(current_dir, test_id)  # Join current directory with test_id
    
    # Create folder if not exists
    os.makedirs(test_dir, exist_ok=True)