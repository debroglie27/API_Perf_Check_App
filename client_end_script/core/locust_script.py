import os
import json
import datetime
from locust.exception import StopUser
from locust import HttpUser,SequentialTaskSet,task

from settings.Answers import answers
from settings.credentials import USER_CREDENTIALS
from settings.config import TEST_SERVER_HOST

from utilities.shared_resources import all_users_complete


class PerfCheck(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)

        # Retrieved the saved safe_uuid environment variable
        self.quiz_id = os.getenv('SAFE_UUID')
        # Retrieved the saved qqc_url environment variable
        self.qqc_url = os.getenv('QQC_URL')

    def on_start(self):
        """Notify the parent user that a task set has started."""
        self.user.last_task_name = None

    def update_last_task(self, task_name):
        """Helper method to update the last task name."""
        self.user.last_task_name = task_name

    @task
    def qqc_url(self):
        self.update_last_task("qqc_url")

        url = self.qqc_url
        with self.client.get(url, name="1.qqc_url", catch_response=True) as response:
            # print(f"quiz_info: {response}")
            pass

    @task
    def login(self):
        self.update_last_task("login")

        self.email, self.password = USER_CREDENTIALS.pop()
        self.client.cookies.clear()
        url = "api/account/login/"
        data = {
            "email_id": self.email,
            "passcode": self.password,
            "web": True,
        }
        with self.client.post(url, name="2.login", data=data, catch_response=True) as response:
            # print(f"login: {response}")
            self.csrftoken = response.cookies['csrftoken']

    @task
    def quiz_info(self):
        self.update_last_task("quiz_info")

        url = "api/quiz/" + self.quiz_id + "/info/"
        with self.client.get(url, name="3.quiz_info", catch_response=True) as response:
            # print(f"quiz_info: {response}")
            response_json = response.json()
            self.quiz_keystate = response_json.get("keystate", None)

    @task
    def quiz_authenticate(self):
        self.update_last_task("quiz_authenticate")

        url = "api/quiz/" + self.quiz_id + "/authenticate/"
        with self.client.get(url, name="4.quiz_authenticate", catch_response=True) as response:
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
            "web": True,
        }
        with self.client.post(url, name="5.quiz_submit", json=data, headers={"X-CSRFToken": self.csrftoken}, catch_response=True) as response:
            # print(f"quiz_submit: {response}")
            pass

    @task
    def done(self):
        # print("A User Completed")
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
