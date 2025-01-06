import os
import time
import requests
from dotenv import load_dotenv

from settings.credentials import DUMMY_STUDENT_CREDENTIAL
from settings.config import COURSE_CODE, TEST_SERVER_HOST, ENV_FILE

# Load environment variables from .env file
load_dotenv(ENV_FILE)

# Retrieve the saved safe_uuid from the .env file
quiz_id = os.getenv('SAFE_UUID')

# Unpacking the DUMMY_STUDENT_CREDENTIAL Tuple
email, password = DUMMY_STUDENT_CREDENTIAL


def login(session, email, password):
    session.cookies.clear()
    url = TEST_SERVER_HOST + "api/account/login/"
    data = {
        "email_id": email,
        "passcode": password,
    }

    try:
        response = session.post(url, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # print("Response Headers:", response.headers)
        # print("Response Body:", response.text)
        csrftoken = response.cookies['csrftoken']
        return csrftoken
    except Exception as e:
        print(f"Error during login: {e}")
        
    return False


def course_list(session):
    url = TEST_SERVER_HOST + "api/course/"

    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return True
    except Exception as e:
        print(f"Error during course_list: {e}")

    return False


def quiz_list(session):
    url = TEST_SERVER_HOST + "api/quiz/" + COURSE_CODE + "/downloadable-quizzes/"
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return True
    except Exception as e:
        print(f"Error during quiz_list: {e}")

    return False


def quiz_info(session, quiz_id):
    url = TEST_SERVER_HOST + "api/quiz/" + quiz_id + "/info/"
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Parse the response text as JSON
        response_json = response.json()
        # Extract the keystate
        quiz_keystate = response_json.get("keystate", False)

        return quiz_keystate
    except Exception as e:
        print(f"Error during quiz_info: {e}")

    return False


def dummy_user():
    session = requests.Session()

    # Step 1: Login
    if not login(session, email, password):
        print("Dummy Student: Login Request Failed!!!")
        exit(1)

    print("Dummy Student: Login Successful")

    time.sleep(1)

    # Step 2: Get course list
    if not course_list(session):
        print("Dummy Student: Course List Failed!!!")
        exit(1)

    print("Dummy Student: Course List Successful")

    time.sleep(1)

    # Step 3: Get quiz list
    if not quiz_list(session):
        print("Dummy Student: Quiz List Failed!!!")
        exit(1)

    print("Dummy Student: Quiz List Successful")

    time.sleep(1)

    # Step 4: Get quiz info
    if not quiz_info(session, quiz_id):
        print("Dummy Student: Quiz Info Failed!!!")
        exit(1)

    print("Dummy Student: Quiz Info Successful")

    time.sleep(1)
