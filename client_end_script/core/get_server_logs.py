import os
import socket
import tarfile
from ftplib import FTP

from settings.config import LOG_HOST, SEARCH_LINES_LIMIT, FTP_SERVER_PORT, SERVER_DAEMON_PORT


def get_server_logs(test_id):
    num_lines_extract = SEARCH_LINES_LIMIT
    # This function fetches and saves the logs in .tar.gz file
    client_run(test_id, LOG_HOST, num_lines_extract)  
    
    # Extract the .tar.gz file
    extract_file = f"{test_id}.tar.gz"
    if tarfile.is_tarfile(extract_file):
        with tarfile.open(extract_file, "r:gz") as tar:
            tar.extractall()  # Extract all contents from the tar.gz file
    
    # Remove the .tar.gz file after extraction
    if os.path.exists(extract_file):
        os.remove(extract_file)


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