import requests
import json
import subprocess

# Define the login URL and login credentials
host = "https://safev2.cse.iitb.ac.in/"
login_url = host+"account/login/"
username = "arijeet_instructor@noemail.none"
password = "safe@123sa"


def login_and_publish_quiz():
    # Create a session to persist cookies across requests
    session = requests.Session()

    # Send a GET request to the login page to retrieve any necessary CSRF tokens
    login_page_response = session.get(login_url)

    # Extract the CSRF token from the response
    csrf_token = session.cookies.get("csrftoken")

    # Prepare the login data with the CSRF token
    login_data = {
        "username": username,
        "password": password,
        "csrfmiddlewaretoken": csrf_token,
    }

    # Perform the login by sending a POST request with the login data
    login_response = session.post(login_url, data=login_data)

    # Check if the login was successful
    if login_response.status_code == 200 :
        print("Login successful!")
    else:
        print("Login failed.")

    # use the session object to make authenticated requests to the website.
    csrf_token = session.cookies.get("csrftoken")
    publish_data = {
        "csrfmiddlewaretoken": csrf_token,
        "type":"flexible",
        "start_time":"T",
        "end_time":"T",
    }
    publish_quiz_url = host+"web_api/quiz/19603/publish-quiz/"
    publish_quiz_response = session.post(publish_quiz_url,data=publish_data)
    print(publish_quiz_response.text)
    publish_response=json.loads(publish_quiz_response.text)
    print(publish_response)
    print(publish_response['safe_uuid'])
    safe_uuid = publish_response['safe_uuid']

    # yet to write start quiz api
    csrf_token = session.cookies.get("csrftoken")
    publish_data = {
        "csrfmiddlewaretoken": csrf_token,
    }
    quiz_id = publish_response['id']
    print("id",quiz_id)
    start_quiz_url = host + f"/web_api/quiz/instance/{quiz_id}/start/" 
    start_quiz_response = session.post(start_quiz_url,data=publish_data)
    print(start_quiz_response.text)

    return safe_uuid


def set_test_name(quiz_uuid):
    command = f"echo {quiz_uuid} | python3 settings/TestName.py"
    subprocess.run(command,shell=True)
    print("\nInitial Script over")

if __name__ =="__main__":
    set_test_name(login_and_publish_quiz())