import os,json,subprocess,argparse,socket,requests
from datetime import datetime
from ftplib import FTP
from configparser import ConfigParser
from math import ceil
from config import LOG_HOST,TEST_SERVER_HOST,CPU_HOST,HTTP_PORT,COMPARE_WITH_PREV_ENTRIES,SEARCH_LINES_LIMIT,FTP_SERVER_PORT,SERVER_DAEMON_PORT,RUN_TIME


def extract_api_specific_logs(filename,dirname):
    with open('APIs.json','r') as f:
        api_info = json.load(f)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for api in api_info:
        command = f"cat {filename} | grep {api['searchTerm']} > {dirname}/{api['APIName']}.logs"
        subprocess.run(command,shell=True)


def extract_historical_data(test_id):
    base_dir=os.getcwd()
    log_data_dir = base_dir+"/logs/resp_time"
    subprocess.run(f"mkdir -p {log_data_dir}",shell=True)
    os.chdir(str(test_id))
    with open('components.json','r') as f:
        components_info = json.load(f)
    timeUnit=""
    tarchdir=""
    count=0
    for item in components_info:
        filename=item["componentName"]+"-"+test_id+".log"
        dirname=item["componentName"]+"-"+test_id
        if (count==0):     
            tarchdir=dirname=item["componentName"]+"-"+test_id
            timeUnit=item["timeUnit"]
        count+=1
        extract_api_specific_logs(filename,dirname)
    

def generate_test_id():
    now=datetime.now()
    custom_format = "%Y-%m-%d_%H-%M-%S"
    test_id = now.strftime(custom_format)
    return test_id


def create_test_directory(test_id):
    current_dir = os.getcwd()
    make_dir=["mkdir",f"{test_id}"]
    subprocess.run(make_dir)


def sys_perf_check(test_id,msg="",num_user=0):
    url = TEST_SERVER_HOST+ f"sys_perf_check/{test_id}-{msg}/{num_user}/"
    requests.get(url)


def performance_test(num_user,ramp_up,test_id):
    sys_perf_check(test_id,"START")
    write_config(test_id,num_user)
    rate=ceil(num_user*ramp_up)
    time=RUN_TIME #seconds
    locust_cmd=["locust","-f","./perfcheck.py",\
        "--headless","-u",f"{num_user}","-r",f"{rate}","-t",f"{time}",\
            "--csv-full-history",f"--csv={test_id}/{num_user}"]
    subprocess.run(locust_cmd)
    sys_perf_check(test_id,"END")
    subprocess.run(["rm","test.ini"])


def command_line_args_apc():
    parser = argparse.ArgumentParser(prog='./client_end_module.py',\
    description='To monitor performance of APIs over time')
    parser.add_argument('-l',metavar="NUMBER_OF_USERS",required=True,type=int,help='Specify the number of users in the performance test')
    parser.add_argument('-r',metavar="RAMP_UP_RATE",default=0.1,type=float,help='Specify the ramp up rate for performance test (between 0 and 1)')
    args = parser.parse_args()
    return args.l,args.r


def get_server_logs(test_id):
    num_lines_extract= SEARCH_LINES_LIMIT
    client_run(test_id,LOG_HOST,num_lines_extract)
    extract_file = str(test_id)+ ".tar.gz"
    subprocess.run(["tar","-xvzf",extract_file])
    subprocess.run(['cp','components.json',test_id])
    subprocess.run(['cp','APIs.json',test_id])


def write_config(test_id,num_users):
    config=ConfigParser()
    config["test"]={
        "test-id":test_id,
        "num-of-users":num_users
    }
    with open("test.ini","w+") as f:
        config.write(f)


def read_config():
    config=ConfigParser()
    config.read("test.ini")
    config_data = config["test"]
    return config_data["test-id"],config_data["num-of-users"]


def client_run(testName,logHost,numLinesExtract):
    message = ["ExtractLogsNew",testName,str(numLinesExtract)]
    extractionStatus=send_client_status(logHost,message)
    if extractionStatus != "ExtractionComplete":
        print("Unable to Extract Logs")
        exit(1)
    print(extractionStatus)
    print("Fetching log files")
    ftp_client(logHost,testName)
    message=["CloseFTPServer"]
    FTPServerStatus=send_client_status(logHost,message)
    if  FTPServerStatus!= "FTPServerClosed":
        print("Unable to close FTP server")
        exit(1)
    print(FTPServerStatus)


def send_client_status(host,message):
    port = SERVER_DAEMON_PORT  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    # if message[0]=="ExtractLogs" or message[0]=="CloseFTPServer":
    message= ",".join(message)
    print(message)
    client_socket.send(message.encode())  # send message
    data = client_socket.recv(1024).decode()  # receive response
    client_socket.close()  # close the connection
    return data
    # else:
    #     print("No message Received at client check for errors")
    #     exit(1)

def ftp_client(host,testName):
    port=FTP_SERVER_PORT
    fileName = testName+".tar.gz"
    ftp = FTP()
    ftp.connect(host,port)
    ftp.login()
    ftp.retrbinary("RETR " +fileName,open(fileName,"wb").write)
    print("log files received")


def constructor_script():
    if os.path.isfile("./initial_script.py"):
        constructor=["python3","initial_script.py"]
        subprocess.run(constructor)
        print()
        print("initial_script executed")
        print()
    else:
        print()
        print("initial_script not used since it is not specified")
        print()
