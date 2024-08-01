# import sys
from locust import HttpUser,SequentialTaskSet,task,constant,events
from locust.exception import StopUser
from client_end_script_helper import read_config
from config import TEST_SERVER_HOST
from credentials import *
from Answers import *
from CourseCode import coursecode
from TestName import quizid
from locust import HttpUser,SequentialTaskSet,task,constant,log
import re
import datetime
# from locust.exception import StopUser

test_id,num_user=read_config()
# url = "sys_perf_check/"+test_id+"/"+num_user+"/"
class PerfCheck(SequentialTaskSet):
    def __init__(self,parent):
        super().__init__(parent)
        self.codeid = quizid
        # print("this test is being conducted for the quiz " + self.codeid)
        # self.email,self.password=USER_CREDENTIALS.pop()

    @task
    def login(self):
        self.email,self.password=USER_CREDENTIALS.pop()
        self.client.cookies.clear()
        url="api/account/login/"
        data={
            "email_id":self.email,
            "anonymous_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjFkYmUwNmI1ZDdjMmE3YzA0NDU2MzA2MWZmMGZlYTM3NzQwYjg2YmMiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9zYWZlLXYyLXNlcnZlciIsImF1ZCI6InNhZmUtdjItc2VydmVyIiwiYXV0aF90aW1lIjoxNzIyNTA2Mjk0LCJ1c2VyX2lkIjoiYkhldTNiWUs5Uk85WmxGbUJUa3RDVEVrZURuMSIsInN1YiI6ImJIZXUzYllLOVJPOVpsRm1CVGt0Q1RFa2VEbjEiLCJpYXQiOjE3MjI1MDYyOTQsImV4cCI6MTcyMjUwOTg5NCwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6e30sInNpZ25faW5fcHJvdmlkZXIiOiJhbm9ueW1vdXMifX0.ZFqZsnIVngd8fhCjFXNFWPLdrizzjYTR3_ekwZoGLFs5k1tt4g5F6flEA39qF7s0ALVLIvLYPUusaF9gXxB5_oDOwcAfhB8dUBIWOCHeAsaG56PCldXXuRT7MIlUyw4gqet8s_Oc894DnLGvNsykBxsGLKyzplxvXDNu3helGRnDVQutJ4ylbXa8cVfVQV78DFkmpvDzWLyGjyKj3bNCAC5eY_1qTkDCX3eyLhhfeav2ZeKBYSF8Z7TzBkMs2usZOD-Nh8CWVS1-OqB9jYARUKowWsNluMDpMCmWMGRKJtWWi_K2xlSfSh3CMLiWhjoqZByXasqOKlCSzHlKfZn9cg",
            "device_reg_token":"dWwDz1OTSkugCctvOhsRi5:APA91bFvcYQxj2BwhuPq9hMB6rVarSFeBFkliwLV21cD0T1e4Xj3cP5XgtYDT77xXDRyC6VCDE8ijPm2eOaIooklDFcixdEzcZUY6IatWjQZPi_6Ssmfwf3w67zvDhNNPdgsYHW_Yv5h",
            "passcode":self.password,
            "version":"a2.9.42",
        }
        with self.client.post(url,name="1.login",data=data,catch_response=True) as response:
            print("login:",response)
            # print(f"login: {response}", file=sys.stderr)
            self.csrftoken = response.cookies['csrftoken']

    @task
    def course_list(self):
        url ="api/course/"
        data = {
            "version":"a2.9.42",
        }
        with self.client.get(url,name="2.course_list",data=data,catch_response=True) as response:
            # print("course_list:",response.text)
            print("course_list:",response)
            self.code = coursecode


    @task
    def quiz_list(self):
        url = "api/quiz/"+ self.code + "/downloadable-quizzes/"
        data = {
            "version":"a2.9.42",
        }
        with self.client.get(url,name="3.quiz_list",data=data,catch_response=True) as response:
            # print("quiz_list:",response.text)
            print("quiz_list:",response)

    @task
    def quiz_info(self):
        url = "api/quiz/"+ self.codeid + "/info/"
        data = {
            "version":"a2.9.42",
        }
        with self.client.get(url,name="4.quiz_info",data=data,catch_response=True) as response:
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
        data = {
            "version":"a2.9.42",
        }
        with self.client.get(url,name="6.quiz_authenticate",data=data,catch_response=True) as response:
            print("quiz_authenticate:",response)

    # @task
    # def upload_image_(self):
    #     url = "api/quiz/uploadImage/"
    #     # attach = open('low.jpg', 'rb')
    #     attach = open('mid.jpg', 'rb')
    #     # attach = open('high.jpg', 'rb')
    #     with self.client.post(url, name="7.upload_image", files=dict(ansimage=attach), headers={"X-CSRFToken": self.csrftoken}, catch_response=True) as response:
    #         print(url+"done")

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

    # @task
    # def perf_check(self):
    #     url = "sys_perf_check/"+test_id+"/"+num_user+"/"
    #     print(url)
    #     # with self.client.get(url,name="perf_check",catch_response=True,verify=False) as response:
    #     with self.client.get(url,name="perf_check",catch_response=True,verify=False) as response:
    #         print("perf_check:",response.text)
            
            


class MySeqTest(HttpUser):
    # fixed_count=1
    wait_time=constant(1)
    host = TEST_SERVER_HOST
    tasks = [PerfCheck]

