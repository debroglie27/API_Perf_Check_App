import os
import json
import requests
from settings.config import TEST_SERVER_HOST, INSTRUCTOR_USERNAME, INSTRUCTOR_PASSWORD


def login_instructor(session):
    """
    Logs in the instructor by sending a POST request with credentials.

    Args:
        session (requests.Session): The session object for making HTTP requests.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    # Define the login URL
    login_url = TEST_SERVER_HOST + "account/login/"

    # Send a GET request to retrieve the login page (to obtain the CSRF token)
    login_page_response = session.get(login_url)

    # Extract the CSRF token from the response cookies
    csrf_token = session.cookies.get("csrftoken")

    # Prepare login data with credentials and CSRF token
    login_data = {
        "username": INSTRUCTOR_USERNAME,
        "password": INSTRUCTOR_PASSWORD,
        "csrfmiddlewaretoken": csrf_token,
    }

    # Perform login by sending a POST request with login data
    login_response = session.post(login_url, data=login_data)

    # Check if the login was successful
    if login_response.status_code == 200:
        print("Instructor Login Successful!")
        return True
    else:
        print("Instructor Login Failed!")
        return False


def publish_quiz(session):
    """
    Publishes the quiz and retrieves the safe UUID and quiz ID from the response.

    Args:
        session (requests.Session): The session object for making HTTP requests.

    Returns:
        str: The safe UUID of the published quiz, or None if publishing fails.
    """
    # Get updated CSRF token
    csrf_token = session.cookies.get("csrftoken")

    # Prepare data for publishing the quiz
    publish_data = {
        "csrfmiddlewaretoken": csrf_token,
        "type": "flexible",
        "start_time": "T",  # Placeholder value for start time
        "end_time": "T",    # Placeholder value for end time
    }

    # Define the URL to publish the quiz
    publish_quiz_url = TEST_SERVER_HOST + "web_api/quiz/19603/publish-quiz/"
    publish_quiz_response = session.post(publish_quiz_url, data=publish_data)

    # Parse the response from publishing the quiz
    publish_response = json.loads(publish_quiz_response.text)

    # Extract the safe UUID, quiz ID and qqc URL from the response
    safe_uuid = publish_response.get('safe_uuid')
    quiz_id = publish_response.get('id')
    qqc_url = publish_response.get('qqc_url')

    return safe_uuid, quiz_id, qqc_url


def start_quiz(session, quiz_id):
    """
    Starts the quiz by sending a POST request with the quiz ID and CSRF token.

    Args:
        session (requests.Session): The session object for making HTTP requests.
        quiz_id (str): The ID of the quiz to be started.

    Returns:
        bool: True if the quiz is successfully started, False otherwise.
    """
    # Get the CSRF token from session cookies
    csrf_token = session.cookies.get("csrftoken")

    # Prepare the data to start the quiz
    start_quiz_data = {
        "csrfmiddlewaretoken": csrf_token,
    }

    # Define the URL for starting the quiz (based on the quiz ID)
    start_quiz_url = TEST_SERVER_HOST + f"/web_api/quiz/instance/{quiz_id}/start/"

    # Send the POST request to start the quiz
    start_quiz_response = session.post(start_quiz_url, data=start_quiz_data)

    # Check the response status
    if start_quiz_response.status_code == 200:
        print(f"Quiz {quiz_id} started successfully!")
    else:
        print(f"Failed to start quiz {quiz_id}. Response: {start_quiz_response.text}")


def save_values(safe_uuid, qqc_url):
    """
    Saves the safe UUID to the .env file.

    Args:
        safe_uuid (str): The safe UUID to be saved.
    """
    # Save these as environment variables
    os.environ["SAFE_UUID"] = safe_uuid
    os.environ["QQC_URL"] = qqc_url

    print("Safe UUID saved as environment variable.")
    print("QQC URL saved as environment variable.")


def initial_setup():
    """
    Main function that calls the other functions to perform the entire flow:
    login, publish the quiz, and save the safe UUID.
    """
    # Create a session to persist cookies and tokens across requests
    session = requests.Session()

    # Step 1: Log in the instructor
    if not login_instructor(session):
        print("Exiting program due to login failure.")
        exit(1)

    # Step 2: Publish the quiz and get the safe UUID
    safe_uuid, quiz_id, qqc_url = publish_quiz(session)

    # Step 3: If safe UUID and qqc URL is successfully retrieved, save it
    if safe_uuid and quiz_id and qqc_url:
        save_values(safe_uuid, qqc_url)
    else:
        print("Exiting program due to failure in publishing the quiz.")
        exit(1)

    # Step 4: Start the quiz using the quiz ID
    if quiz_id:
        start_quiz(session, quiz_id)
    else:
        print("Exiting program due to missing quiz ID.")
        exit(1)


if __name__ == "__main__":
    initial_setup()