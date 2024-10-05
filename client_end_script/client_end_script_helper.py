import os,json,subprocess,argparse,socket,requests
from datetime import datetime
from ftplib import FTP
from math import ceil
from settings.config import LOG_HOST,TEST_SERVER_HOST,SEARCH_LINES_LIMIT,FTP_SERVER_PORT,SERVER_DAEMON_PORT


def extract_api_specific_logs(filename,dirname):
    with open('settings/APIs.json','r') as f:
        api_info = json.load(f)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for api in api_info:
        command = f"cat {filename} | grep {api['searchTerm']} > {dirname}/{api['APIName']}.logs"
        subprocess.run(command,shell=True)


def extract_data(test_id):
    with open('settings/components.json','r') as f:
        components_info = json.load(f)
    
    for item in components_info:
        filename=test_id+"/"+item["componentName"]+"-"+test_id+".log"
        dirname=test_id+"/"+item["componentName"]

        extract_api_specific_logs(filename,dirname)
    

def generate_test_id():
    now=datetime.now()
    custom_format = "%Y-%m-%d_%H-%M-%S"
    test_id = now.strftime(custom_format)
    return test_id


def create_test_directory(test_id):
    current_dir = os.getcwd()  # Get current working directory
    test_dir = os.path.join(current_dir, test_id)  # Join current directory with test_id
    make_dir = ["mkdir", test_dir]  # Use the full path for the directory
    subprocess.run(make_dir)


def sys_perf_check(test_id,msg="",num_user=0):
    url = TEST_SERVER_HOST+ f"sys_perf_check/{test_id}-{msg}/{num_user}/"
    requests.get(url)


def performance_test(num_user,ramp_up,duration,test_id):
    sys_perf_check(test_id,"START")
    # write_config(test_id,num_user)
    rate=ceil(num_user*ramp_up)
    locust_cmd=["locust","-f","./perfcheck.py",\
        "--headless","-u",f"{num_user}","-r",f"{rate}","-t",f"{duration}",\
            "--csv-full-history",f"--csv={test_id}/{num_user}"]
    subprocess.run(locust_cmd)
    sys_perf_check(test_id,"END")
    # subprocess.run(["rm","test.ini"])


def command_line_args_apc():
    parser = argparse.ArgumentParser(prog='./client_end_module.py',\
    description='To monitor performance of APIs over time')
    parser.add_argument('-l',metavar="NUM_OF_USERS",required=True,type=int,help='The number of users to simulate during the performance test')
    parser.add_argument('-r',metavar="RAMP_UP_RATE",default=0.1,type=float,help='The ramp up rate for performance test (between 0 and 1)')
    parser.add_argument('-t',metavar="DURATION",default=60,type=int,help='The duration for the locust loadtest')
    args = parser.parse_args()
    return args.l, args.r, args.t


def get_server_logs(test_id):
    num_lines_extract = SEARCH_LINES_LIMIT
    client_run(test_id, LOG_HOST, num_lines_extract)
    
    # Extract the .tar.gz file
    extract_file = str(test_id) + ".tar.gz"
    subprocess.run(["tar", "-xvzf", extract_file])
    
    # Remove the .tar.gz file after extraction
    subprocess.run("rm *.tar.gz", shell=True)


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

    message= ",".join(message)
    print(message)
    client_socket.send(message.encode())  # send message
    data = client_socket.recv(1024).decode()  # receive response
    client_socket.close()
    return data


def ftp_client(host,testName):
    port=FTP_SERVER_PORT
    fileName = testName+".tar.gz"
    ftp = FTP()
    ftp.connect(host,port)
    ftp.login()
    ftp.retrbinary("RETR " +fileName,open(fileName,"wb").write)
    print("log files received")
