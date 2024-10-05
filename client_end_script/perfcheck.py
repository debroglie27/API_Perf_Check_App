import os
import re
import datetime
from locust import HttpUser,SequentialTaskSet,task,constant
from locust.exception import StopUser
from settings.config import TEST_SERVER_HOST, COURSE_CODE, ENV_FILE
from settings.credentials import USER_CREDENTIALS
from settings.Answers import answers
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(ENV_FILE)

# Retrieve the saved safe_uuid from the .env file
safe_uuid = os.getenv('SAFE_UUID')


class PerfCheck(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.quiz_id = safe_uuid

    @task
    def login(self):
        self.email, self.password = USER_CREDENTIALS.pop()
        self.client.cookies.clear()
        url = "api/account/login/"
        data = {
            "email_id": self.email,
            "passcode": self.password,
        }
        with self.client.post(url, name="1.login", data=data, catch_response=True) as response:
            # print(f"login: {response}")
            self.csrftoken = response.cookies['csrftoken']

    @task
    def course_list(self):
        url = "api/course/"
        with self.client.get(url, name="2.course_list", catch_response=True) as response:
            # print(f"course_list: {response}")
            self.code = COURSE_CODE

    @task
    def quiz_list(self):
        url = "api/quiz/" + self.code + "/downloadable-quizzes/"
        with self.client.get(url, name="3.quiz_list", catch_response=True) as response:
            # print(f"quiz_list: {response}")
            pass

    @task
    def quiz_info(self):
        url = "api/quiz/" + self.quiz_id + "/info/"
        with self.client.get(url, name="4.quiz_info", catch_response=True) as response:
            # print(f"quiz_info: {response}")
            quiz_keystate = re.search(r"\"keystate\":(.*?)(,|})", response.text)
            self.quiz_keystate = quiz_keystate.group(1)[1:-1]
            # print(f"quiz_keystate: {self.quiz_keystate}")

    @task
    def quiz_download(self):
        url = "api/quiz/" + self.quiz_id + "/download/"
        with self.client.get(url, name="5.quiz_download", catch_response=True) as response:
            # print(f"quiz_download: {response}")
            pass

    @task
    def quiz_authenticate(self):
        url = "api/quiz/" + self.quiz_id + "/authenticate/"
        with self.client.get(url, name="6.quiz_authenticate", catch_response=True) as response:
            # print(f"quiz_authenticate: {response}")
            pass

    @task
    def quiz_submit(self):
        datetime_format = "%Y-%m-%dT%H:%M:%S"
        url = "api/quiz/" + self.quiz_keystate + "/submit/"
        data = {
            "quizData": answers,
            "submissionTime": datetime.datetime.now().strftime(datetime_format),
            "seconds_since_mark": "0",
        }
        with self.client.post(url, name="7.quiz_submit", json=data, headers={"X-CSRFToken": self.csrftoken}, catch_response=True) as response:
            # print(f"quiz_submit: {response}")
            pass

    @task
    def done(self):
        raise StopUser()


class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = TEST_SERVER_HOST
    tasks = [PerfCheck]