import os,json,metrohash,subprocess,argparse,csv,re,socket,csv,tkinter as tk,requests
from datetime import datetime
from ftplib import FTP
from configparser import ConfigParser
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk
from PIL import ImageTk, Image
from math import ceil
from time import sleep
import numpy as np
import sqlite3
import scipy.stats as stats
from colorama import Fore, Style
from scipy.stats import mannwhitneyu
from scipy import stats
from config import LOG_HOST,TEST_SERVER_HOST,CPU_HOST,HTTP_PORT,COMPARE_WITH_PREV_ENTRIES,SEARCH_LINES_LIMIT,FTP_SERVER_PORT,SERVER_DAEMON_PORT,RUN_TIME


DB_FILE = "testdates.db"
def get_util_list(num):
    lst=[]
    in_file=str(num)+"_users.txt"
    out_file=str(num)+".csv"
    command = "awk -F' ' '{print $2\",\"$3}' "+in_file+" > "+out_file
    subprocess.run(command,shell=True)

    lst.append(str(num))
    with open(out_file,'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            lst.append(row[1])
    return lst

def get_util_header(num):
    lst=[]
    out_file=str(num)+".csv"

    lst.append("num_of_users")
    with open(out_file,'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if(row[0]=="all"):
                lst.append(row[0])
            else:
                lst.append("core:"+row[0])
    return lst


def generate_utilization_csv(low,upper,step):
    write_lst=[]
    os.chdir("./cpu_utilization")
    for num in range(low,upper+1,step):
        write_lst.append(get_util_list(num))
        # get_util_list(num)
    write_lst.insert(0,get_util_header(low))
    cpu_util_file="cpu_util.csv"
    with open(cpu_util_file,'w+') as file:
        for row in write_lst:
            file.write(",".join(row) +"\n")
    os.chdir("..")
    for row in write_lst:
        print(row)

def extract_api_specific_logs(filename,dirname):
    with open('APIs.json','r') as f:
        api_info = json.load(f)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for api in api_info:
        command = f"cat {filename} | grep {api['searchTerm']} > {dirname}/{api['APIName']}.logs"
        subprocess.run(command,shell=True)

def extract_data(test_id):
    os.chdir(str(test_id))
    f = open('components.json')
    components_info = json.load(f)
    f.close()
    for item in components_info:
        filename=item["componentName"]+"-"+test_id+".log"
        dirname=item["componentName"]+"-"+test_id
        extract_api_specific_logs(filename,dirname)
    
    ### deba iske aage tu bana
    print(os.getcwd())
    file_lst=[]
    for item in components_info:
        print(item["componentName"]+"-"+test_id+".log")
        res=item["componentName"]+"-"+test_id+".log"
        file_lst.append([res,item["timeUnit"]])
    for file in file_lst:
        print(file)
        id_pattern=test_id
        extract_time(id_pattern,file[0],file[1])
        
        
        
def set_up_db():
    if os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} already exists")
        return
    print(f"Creating Database {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time DATETIME
    ) 
    ''')
    conn.commit()
    conn.close()

def get_auto_test_id():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    select seq from sqlite_sequence 
    ''')
    val = cursor.fetchall()
    res=1
    if len(val)>0:
        res = val[0][0]+1
    conn.commit()
    conn.close()
    return res

def write_to_csv(test_id,api,path,response_time_lst):
    test_id=str(test_id)
    filename=test_id+"_"+api
    # Define the file path
    file_path = path +"/"+filename+".csv"

    # Open the CSV file in write mode
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the lst to the CSV file
        for num in response_time_lst:
            writer.writerow([num])

def read_from_csv(test_id,api,path):
    test_id=str(test_id)
    response_time_lst=[]
    filename=test_id+"_"+api
    file_path = path +"/"+filename + ".csv"

    # Open the CSV file in read mode
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            # Iterate through the rows and convert each value to a float
            for row in reader:
                response_time_lst.append(float(row[0]))
    except FileNotFoundError:
        return response_time_lst
    return response_time_lst

def print_performance(code):
    if code == "1":
        print(f"{Fore.LIGHTBLACK_EX}{Style.BRIGHT}.{Style.RESET_ALL}",end='')
    elif code == "2":
        print(f"{Fore.RED}{Style.BRIGHT}-{Style.RESET_ALL}",end='')
    elif code == "3":
        print(f"{Fore.GREEN}{Style.BRIGHT}+{Style.RESET_ALL}",end='')
    elif code == "4":
        print(f"{Fore.LIGHTBLACK_EX}{Style.BRIGHT}={Style.RESET_ALL}",end='')

def t_test_result(curr_lst,old_lst):
    """
        1 - comparison not possible as old data does not exist
        2 - Performance decreased compared to prev entry
        3 - Performance improved compared to prev entry
        4 - Almost similar Performance . We can not reject the null hypothesis
    """
    print("t test used")
    if len(old_lst) == 0:
        return "1"
    if len(curr_lst) == 0:
        raise ValueError("Response time for current test not generated")
    t_stats,p_val = stats.ttest_ind(old_lst,curr_lst)
    print("the t value is "+str(t_stats)+"the p value is "+str(p_val))
    alpha = 0.01
    if p_val >=alpha:
        return "4"
    if t_stats <= 0:
        return "3"
    return "2"
def man_u_test_result(curr_lst,old_lst):
    """
        1 - comparison not possible as old data does not exist
        2 - Performance decreased compared to prev entry
        3 - Performance improved compared to prev entry
        4 - Almost similar Performance . We can not reject the null hypothesis
    """
    print("u test used")
    if len(old_lst) == 0:
        return "1"
    if len(curr_lst) == 0:
        raise ValueError("Response time for current test not generated")
    statistic, p_val = mannwhitneyu(old_lst, curr_lst)
    hodges_lehmann_estimate = np.median([y - x for x in old_lst for y in curr_lst])
    # t_stats,p_val = stats.ttest_ind(old_lst,curr_lst)
    print("the hodges lehmann estimate value is "+str(hodges_lehmann_estimate)+"the p value is "+str(p_val))
    alpha = 0.01
    if p_val >=alpha:
        return "4"
    if hodges_lehmann_estimate <= 0:
        return "3"
    return "2"
    
def normality_test(curr_l):
    print("Normality check")
    try:
        statistic, p_value = stats.shapiro(curr_l)
        alpha = 0.05
        if p_value > alpha:
            return 1
            # print("Sample looks Gaussian (fail to reject H0)")
        else:
            return 0
            # print("Sample does not look Gaussian (reject H0)")
    except ValueError:
        return 0 # go for non gaussian

def generate_t_test_results(db_test_id,log_path):
    print(db_test_id)
    headers= ["API Name","Avg. Resp Time","std deviation"]
    listofhead=[]
    h1=["API Name","Average Response Time (ms) Present","Standard deviation (ms) Present"]
    for val in COMPARE_WITH_PREV_ENTRIES:
        headers.append(""+str(val)+" P.E.")
        listofhead.append (str(val)+" P.E")
        h1.append("Average Response Time (ms) "+str(val)+" P.E")
        h1.append("Standard deviation (ms) "+str(val)+" P.E")
    res = []
    res.append(headers)
    
    test_report=[]
    # h1=["API Name","Avg. Resp Time Present","std deviation Present","Avg. Resp Time "+ listofhead[0],"std deviation "+ listofhead[0],"Avg. Resp Time "+ listofhead[1],"std deviation "+listofhead[1],"Avg. Resp Time "+listofhead[2],"std deviation "+ listofhead[2]]
    test_report.append(h1)
    with open('APIs.json','r') as f:
        api_info = json.load(f)
    apilist=[]
    for item in api_info:
        filename=item["APIName"]
        apilist.append(filename)
    for apiname in apilist:
        api_res=[]
        api_info=[]
        api_rt_lst = read_from_csv(db_test_id,apiname,log_path) # response time
        api_mean = int(round(np.mean(api_rt_lst)))
        api_std_dev = int(round(np.std(api_rt_lst)))
        api_info.append(apiname)
        print("========================================================================")
        print("this test is for "+apiname+"api")
        api_info.append(str(api_mean))
        api_info.append(str(api_std_dev))
        api_res.append(apiname)
        api_res.append(str(api_mean))
        api_res.append(str(api_std_dev))
        for val in COMPARE_WITH_PREV_ENTRIES:
            prev_id = db_test_id-val
            prev_rt_lst = read_from_csv(prev_id,apiname,log_path)
            lengthprev=len(prev_rt_lst)
            if(lengthprev==0):
                api_res.append("N.A")
                api_res.append("N.A")
            else:
                a_m = int(round(np.mean(prev_rt_lst)))
                a_dev = int(round(np.std(prev_rt_lst)))
                api_res.append(str(a_m))
                api_res.append(str(a_dev))
            print("the prev id is staring here and comparison is performed for "+str(val)+" days ago")
            print(prev_id)
            normal_1= normality_test(api_rt_lst)
            normal_2=normality_test(prev_rt_lst)
            if (normal_1 and normal_2):
                t_res=t_test_result(api_rt_lst,prev_rt_lst)
            else:
                t_res=man_u_test_result(api_rt_lst,prev_rt_lst)
            # t_res=t_test_result(api_rt_lst,prev_rt_lst)
            api_info.append(str(t_res))
        res.append(api_info)
        test_report.append(api_res)
        
    csv_file = "testreport.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(test_report)
    # print(test_report)
    return res

def test_id_to_time(test_id):
    test_id = test_id.split("_")
    _date = test_id[0]
    _time = test_id[1]
    _time = ':'.join(_time.split('-'))
    test_id=[_date,_time]
    test_id = " ".join(test_id)
    return test_id

def insert_test_in_db(test_id):
    test_id = test_id_to_time(test_id)
    conn = sqlite3.connect(DB_FILE)
    print(test_id)
    cursor = conn.cursor()
    query = "INSERT INTO test(time) VALUES ('" + test_id +"')"
    cursor.execute(query)
    conn.commit()
    conn.close()

def print_test_results(result):
    max_len_each_col=[]
    for col in range(len(result[0])):
        max_col_len=0
        for row in range(len(result)):
            max_col_len=max(max_col_len,len(result[row][col]))
        max_len_each_col.append(max_col_len)

    for row in range(len(result)):
        for col in range(len(result[0])):
            if row ==0 or col < 3:
                if col < len(result[0])-1:
                    print("| "+result[row][col]+
                        " "*(max_len_each_col[col]-len(result[row][col])),end=" ")
                else:
                    print("| "+result[row][col]+
                        " "*(max_len_each_col[col]-len(result[row][col]))+" |")
            else:
                if col < len(result[0])-1:
                    print("| ",end="")
                    print_performance(result[row][col])
                    print(" "*(max_len_each_col[col]-len(result[row][col])),end=" ")
                else:
                    print("| ",end="")
                    print_performance(result[row][col])
                    print(" "*(max_len_each_col[col]-len(result[row][col]))+" |")


def extract_historical_data(test_id):
    set_up_db()
    db_test_id = get_auto_test_id()
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

    with open('APIs.json','r') as f:
        api_info = json.load(f)
    apilist=[]
    for item in api_info:
        filename=item["APIName"]
        apilist.append(filename)
    
    os.chdir(tarchdir)
    head=['Date-time','Apiname','Mean','Standard-deviation']
    # print(head)
    data=[]
    # curr_test_id = get_test_id()
    for filename in apilist:
        response_time_pattern = re.compile("\*\*\*.*\*\*\*")
        responsetime=[]
        tempname=filename
        filename=filename+".logs"
        with open(filename) as file_h:
            for line in file_h:
                try:
                    response_time=float(response_time_pattern.search(line).group(0)[3:][:-3])
                    if (timeUnit=="s"):
                        responsetime.append(response_time*1000)
                except AttributeError :
                    if response_time == None:
                        print("AttributeError")
                        exit(1)
        write_to_csv(db_test_id,tempname,log_data_dir,responsetime)
        mean = np.mean(responsetime)
        mean=round(mean, 2)
        std_dev = np.std(responsetime)
        std_dev=round(std_dev, 2)
        data.append([test_id,tempname,str(mean),str(std_dev)])
        # print(mean)
        # print(std_dev)
    os.chdir('../..')
    print(test_id)
    insert_test_in_db(test_id)
    result = generate_t_test_results(db_test_id,log_data_dir)
    print_test_results(result)
    outfile="results.csv"
    if not os.path.exists(outfile):
        with open(outfile, 'w') as csvfile:
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(head) 
            csvwriter.writerows(data)
    else: 
        with open(outfile, 'a') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            # csvwriter.writerow(head) 
            csvwriter.writerows(data)
    print("datawrite completed")
    

def generate_test_id():
    now=datetime.now()
    custom_format = "%Y-%m-%d_%H-%M-%S"
    test_id = now.strftime(custom_format)
    return test_id

def create_test_directory(test_id):
    current_dir = os.getcwd()
    make_dir=["mkdir",f"{test_id}"]
    subprocess.run(make_dir)

def get_cpu_files(lower,upper,step):
    create_dir=["mkdir","-p","cpu_utilization"]
    subprocess.run(create_dir)
    os.chdir("cpu_utilization")
    for users in range(lower,upper+1,step):
        file_name=str(users)+"_users"+".txt"
        file_address="http://"+CPU_HOST+":"+str(HTTP_PORT)+"/"+file_name
        get_file=["curl",file_address]
        response = subprocess.run(get_file,capture_output=True,text=True)
        print("hit")    
        if(response.returncode !=0 ):
            print(get_file)
            print(response.stderr)
            print("HTTP server is not working correctly")
            input()
        else:
            print("get_cpu_files",file_name)
            f = open(file_name,"w+")
            f.write(response.stdout)
            f.close()
    os.chdir("..")

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

def extract_time(id_pattern,file_name,timeUnit):
    s=file_name.split(".")
    head=['Numusers','Averagetime']
    head1=['Responsetime']
    data=[]
    data1=[]
    outfile=s[0]+"restime.csv"
    outputfile=s[0]+".csv"
    print(outputfile)
    only_id_pattern=re.compile(id_pattern)
    id_pattern="/"+id_pattern+"/"+"[0-9]+"
    num_users_pattern = re.compile(id_pattern)
    response_time_pattern = re.compile("\*\*\*.*\*\*\*")
    current_users=-1
    with open(file_name) as file_h:
        count=0
        time=0
        for line in file_h:
            try:
                if line.strip()!="":
                    users=int(num_users_pattern.search(line).group(0)[18:])
                    if current_users==-1:
                        current_users=users
                    if current_users!=users:
                        avg_time=time/count
                        #print(str(current_users)+","+str(avg_time))
                        if (timeUnit=="s"):
                            avg_time=avg_time*1000
                            avg_time = round(avg_time,2)
                            data.append([str(current_users),str(avg_time)])
                        else:
                            avg_time = round(avg_time,2)
                            data.append([str(current_users),str(avg_time)])
                        current_users=users
                        count=0
                        time=0
                    response_time=float(response_time_pattern.search(line).group(0)[3:][:-3])
                    if (timeUnit=="s"):
                        data1.append([str(response_time*1000)])
                    else:
                        data1.append([str(response_time)])
                    count+=1
                    time+=response_time
            except AttributeError :
                if only_id_pattern.search(line) == None:
                    print(line)
                    print("AttributeError")
                    exit(1)
        avg_time=time/count
        if (timeUnit=="s"):
            avg_time=avg_time*1000
            avg_time = round(avg_time,2)
            data.append([str(current_users),str(avg_time)])
        else:
            avg_time = round(avg_time,2)
            data.append([str(current_users),str(avg_time)])
    with open(outfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(head1) 
        csvwriter.writerows(data1)
    with open(outputfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(head) 
        csvwriter.writerows(data)

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

def send_client_status_no_receive(host,message):
    port = SERVER_DAEMON_PORT  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message= ",".join(message)
    print(message)
    client_socket.send(message.encode())  # send message

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

def showGraph(test_id):
    file_lst=[]
    y_list=[]
    components=[]
    f = open('components.json')
    data = json.load(f)
    for i in data:
        res=i["componentName"]+"-"+test_id+".csv"
        file_lst.append(res)
        y_list.append("y_"+i["componentName"])
        components.append(i["componentName"])
    # Closing file
    f.close()
    for i in range(len(file_lst)):
        var=pd.read_csv(file_lst[i])
        y_list[i]=list(var['Averagetime'])
    
    for p in y_list:
        p.insert(0,0)

    x = list(var['Numusers'])
    x.insert(0,0)
    plt.figure(0)
    for i in range(len(y_list)):
        plt.plot(x,y_list[i],marker='o',label=components[i])

    plt.grid(True)
    plt.legend(loc='best')
    plt.xlabel("Number of users")
    plt.ylabel("Response time (ms)")
    resultimage=test_id+".png"
    plt.savefig(resultimage)

def showgui(test_id):
    result=test_id+".png"
    window = tk.Tk()
    window.title("Image and Table Presentation")

    # # Set a colored background
    background_color = "#FF7A7A"  # Specify the desired background color

    canvas = tk.Canvas(window)
    # canvas.configure(bg=background_color)
    canvas.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)


    # Create a Scrollbar widget
    scrollbar = tk.Scrollbar(window, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Canvas to use the Scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)


    # Create a Frame inside the Canvas to hold the content




    frame = tk.Frame(canvas,bg=background_color,bd=10)


    canvas.create_window((0,0), window=frame, anchor=tk.NW,width=1835)


    heading_label = tk.Label(frame, text="Image and Table Presentation", font=("Arial", 40, "bold"), fg="black",bg=background_color)
    heading_label.pack()
    heading_label.pack(pady=10)


    image = Image.open(result)
    image = image.resize((800, 600))  # Resize the image if needed
    photo = ImageTk.PhotoImage(image)
    image_label = ttk.Label(frame, image=photo, borderwidth=2, relief="solid")
    # image_label.place(x=50, y=100)  # Customize the position of the image label
    image_label.pack(expand=True)
    # image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    image_label.pack()
    image_label.pack(pady=10)



    heading_label1 = tk.Label(frame, text="Table containing Response Time(ms) vs number of users ", font=("Arial", 40, "bold"), fg="black",bg=background_color)
    heading_label1.pack()
    heading_label1.pack(pady=10,padx=30)


    # merging the csv files# Read the CSV files into DataFrames
    columns=["Numusers"]
    merged_data = pd.DataFrame()
    f = open('components.json')
    data = json.load(f)

    for i in data:
        columns.append(i["componentName"]+"_time(ms)")
        res=i["componentName"]+"-"+test_id+".csv"
        df = pd.read_csv(res)
        if len(merged_data)== 0:
            merged_data = df
        else:
            # print(df.columns)
            merged_data = pd.merge(merged_data,df, on=df.columns[0])

    table = ttk.Treeview(frame)

    style = ttk.Style()

    style.configure("Treeview.Heading",
                    font=('Arial', 20, 'bold'),  # Set the font size for headers
                    anchor="center",
                    borderwidth=1,
                    relief="solid") 
    style.configure("Treeview",
                    font=('Arial', 16),  # Set the font size
                    anchor="center",
                    borderwidth=1,
                    relief="solid")     # Set alignment to center

    style.configure("Custom.Treeview.Cell",
                    borderwidth=1,
                    relief="solid")
    table['columns'] = columns

    table.heading('#0', text='Index')
    for column in columns:
        table.heading(column, text=column)
    for row in merged_data.itertuples(index=False):
        table.insert("", tk.END, values=row)
        table.insert("", tk.END)
    for column in table["columns"]:
        table.column(column, anchor="center")
    table.configure(show="headings")  # Hide the first empty column
    table.configure(height=25)
    table.pack(fill="both",expand="True")
    table.pack(pady=(10,50),padx=80)
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox(tk.ALL))
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    window.mainloop()

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
