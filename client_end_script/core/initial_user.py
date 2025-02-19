import os
import time
import requests

from settings.credentials import INITIAL_STUDENT_CREDENTIAL
from settings.config import TEST_SERVER_HOST


def qqc_url(session):
    url = os.getenv('QQC_URL')
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return True
    except Exception as e:
        print(f"Error during quiz_info: {e}")

    return False


def login(session, email, password):
    session.cookies.clear()
    url = TEST_SERVER_HOST + "api/account/login/"
    data = {
        "email_id": email,
        "passcode": password,
        "web": True,
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


def initial_user():
    session = requests.Session()

    # Step 1: qqc_url
    if not qqc_url(session, email, password):
        print("Initial Student: qqc_url Request Failed!!!")
        exit(1)

    print("Initial Student: qqc_url Successful")

    # Unpacking the INITIAL STUDENT CREDENTIAL Tuple
    email, password = INITIAL_STUDENT_CREDENTIAL

    # Step 2: Login
    if not login(session, email, password):
        print("Initial Student: Login Request Failed!!!")
        exit(1)

    print("Initial Student: Login Successful")

    time.sleep(1)

    # Retrieve the saved safe_uuid environment variable
    quiz_id = os.getenv('SAFE_UUID')

    # Step 3: Get quiz info
    if not quiz_info(session, quiz_id):
        print("Initial Student: Quiz Info Failed!!!")
        exit(1)

    print("Initial Student: Quiz Info Successful")

    time.sleep(1)