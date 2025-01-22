from datetime import datetime

from utilities.create_directory import create_directory


def generate_test_id():
    now = datetime.now()
    custom_format = "%Y-%m-%d_%H-%M-%S"
    test_id = now.strftime(custom_format)

    # Creating a directory with name test_id where all the results for that test will be stored
    create_directory(test_id)

    return test_id