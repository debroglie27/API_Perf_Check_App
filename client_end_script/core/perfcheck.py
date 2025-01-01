import os
import re
import json
import datetime
from dotenv import load_dotenv
from locust.exception import StopUser
from locust import HttpUser,SequentialTaskSet,task

from settings.Answers import answers
from settings.credentials import USER_CREDENTIALS
from settings.config import TEST_SERVER_HOST, COURSE_CODE, ENV_FILE

from utilities.shared_resources import all_users_complete

# Load environment variables from .env file
load_dotenv(ENV_FILE)

# Retrieve the saved safe_uuid from the .env file
quiz_id = os.getenv('SAFE_UUID')


class PerfCheck(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.quiz_id = quiz_id

    def on_start(self):
        """Notify the parent user that a task set has started."""
        self.user.last_task_name = None

    def update_last_task(self, task_name):
        """Helper method to update the last task name."""
        self.user.last_task_name = task_name

    @task
    def login(self):
        self.update_last_task("login")

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
        self.update_last_task("course_list")

        url = "api/course/"
        with self.client.get(url, name="2.course_list", catch_response=True) as response:
            # print(f"course_list: {response}")
            self.code = COURSE_CODE

    @task
    def quiz_list(self):
        self.update_last_task("quiz_list")

        url = "api/quiz/" + self.code + "/downloadable-quizzes/"
        with self.client.get(url, name="3.quiz_list", catch_response=True) as response:
            # print(f"quiz_list: {response}")
            pass

    @task
    def quiz_info(self):
        self.update_last_task("quiz_info")

        url = "api/quiz/" + self.quiz_id + "/info/"
        with self.client.get(url, name="4.quiz_info", catch_response=True) as response:
            # print(f"quiz_info: {response}")
            quiz_keystate = re.search(r"\"keystate\":(.*?)(,|})", response.text)
            self.quiz_keystate = quiz_keystate.group(1)[1:-1]
            # print(f"quiz_keystate: {self.quiz_keystate}")

    @task
    def quiz_download(self):
        self.update_last_task("quiz_download")

        url = "api/quiz/" + self.quiz_id + "/download/"
        with self.client.get(url, name="5.quiz_download", catch_response=True) as response:
            # print(f"quiz_download: {response}")
            pass

    @task
    def quiz_authenticate(self):
        self.update_last_task("quiz_authenticate")

        url = "api/quiz/" + self.quiz_id + "/authenticate/"
        with self.client.get(url, name="6.quiz_authenticate", catch_response=True) as response:
            # print(f"quiz_authenticate: {response}")
            pass

    @task
    def quiz_submit(self):
        self.update_last_task("quiz_submit")

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
        print("A User Completed")
        all_users_complete.release()
        raise StopUser()


class MySeqTest(HttpUser):
    host = TEST_SERVER_HOST
    tasks = [PerfCheck]

    last_task_name = None  # Attribute to store the last task name

    # Load task-specific wait times from JSON file
    def __init__(self, parent):
        super().__init__(parent)
        current_dir = os.getcwd()
        wait_times_filepath = os.path.join(current_dir, "settings", "task_wait_times.json")
        with open(wait_times_filepath, "r") as f:
            self.task_wait_times = json.load(f)

    # Custom wait_time function
    def wait_time(self):
        """Override wait_time to provide task-specific delays."""

        if self.last_task_name:
            # Default to 1 second if last_task_name not in task_wait_times
            wait = self.task_wait_times.get(self.last_task_name, 1)
            # print(f"\nTask {self.last_task_name} completed. Waiting for {wait} seconds.")

            return wait
        
        # No last task, so apply default wait time
        default_wait_time = 0
        # print(f"\nNo last task. Default wait time applied of {default_wait_time} seconds.")

        return default_wait_time
