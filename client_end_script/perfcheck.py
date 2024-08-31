from locust import HttpUser,SequentialTaskSet,task,constant,events,log
from locust.exception import StopUser
from client_end_script_helper import read_config
from config import TEST_SERVER_HOST
from credentials import *
from Answers import *
from CourseCode import coursecode
from TestName import quizid
import re
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

test_id,num_user=read_config()
class PerfCheck(SequentialTaskSet):
    def __init__(self,parent):
        super().__init__(parent)
        self.codeid = quizid

    @task
    def login(self):
        self.email,self.password=USER_CREDENTIALS.pop()
        self.client.cookies.clear()
        url="api/account/login/"
        data={
            "email_id":self.email,
            "passcode":self.password,
        }
        with self.client.post(url,name="1.login",data=data,catch_response=True) as response:
            logger.info(f"login request: {response}")
            # print(f"login: {response}", file=sys.stderr)
            self.csrftoken = response.cookies['csrftoken']

    @task
    def course_list(self):
        url ="api/course/"
        with self.client.get(url,name="2.course_list",catch_response=True) as response:
            # print("course_list:",response.text)
            print("course_list:",response)
            self.code = coursecode


    @task
    def quiz_list(self):
        url = "api/quiz/"+ self.code + "/downloadable-quizzes/"
        with self.client.get(url,name="3.quiz_list",catch_response=True) as response:
            # print("quiz_list:",response.text)
            print("quiz_list:",response)

    @task
    def quiz_info(self):
        url = "api/quiz/"+ self.codeid + "/info/"
        with self.client.get(url,name="4.quiz_info",catch_response=True) as response:
            quiz_keystate = re.search(r"\"keystate\":(.*?)(,|})",response.text)
            self.quiz_keystate= quiz_keystate.group(1)[1:-1] #.encode('ascii')
            print("quiz_keystate:",self.quiz_keystate)
            
    @task
    def quiz_download(self):
        url = "api/quiz/"+ self.codeid + "/download/"
        with self.client.get(url,name="5.quiz_download",catch_response=True) as response:
            print("quiz_download:",response)
            # print("quiz_download:",response.text)

    @task
    def quiz_authenticate(self):
        url = "api/quiz/"+ self.codeid + "/authenticate/"
        with self.client.get(url,name="6.quiz_authenticate",catch_response=True) as response:
            print("quiz_authenticate:",response)


    @task
    def quiz_submit(self):
            datetime_format = "%Y-%m-%dT%H:%M:%S"
            url = "api/quiz/"+self.quiz_keystate + "/submit/"
            data ={
                "quizData":answers,"submissionTime":datetime.datetime.now().strftime(datetime_format),"seconds_since_mark":"0"
            }
            with self.client.post(url,name="7.quiz_submit",json=data,headers={"X-CSRFToken": self.csrftoken},catch_response=True) as response:
                print("quiz_submit:",response)
                print("quiz_submit:",response.text)

    @task
    def done(self):
        raise StopUser()
            
            


class MySeqTest(HttpUser):
    # fixed_count=1
    wait_time=constant(1)
    host = TEST_SERVER_HOST
    tasks = [PerfCheck]

