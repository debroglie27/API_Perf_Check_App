from client_end_script_helper import extract_historical_data,set_up_db,get_auto_test_id,DB_FILE
import sqlite3
import csv

# def insertions():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO test (time) VALUES ('2023-10-30 13:40:34')")
#     val = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     pass
# set_up_db()
# insertions()
# get_auto_test_id()

######################################################################################################
# test_id='2023-10-21_17-31-02'
# extract_historical_data(test_id)
######################################################################################################

# def write_to_csv(test_id,api,path,response_time_lst):
#     test_id=str(test_id)
#     filename=test_id+"_"+api
#     # Define the file path
#     file_path = path +"/"+filename+".csv"

#     # Open the CSV file in write mode
#     with open(file_path, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         # Write the lst to the CSV file
#         for num in response_time_lst:
#             writer.writerow([num])

# def read_from_csv(test_id,api,path):
#     test_id=str(test_id)
#     response_time_lst=[]
#     print(type(test_id),type(api))
#     filename=test_id+"_"+api
#     file_path = path +"/"+filename + ".csv"

#     # Open the CSV file in read mode
#     with open(file_path, mode='r') as file:
#         reader = csv.reader(file)
#         # Iterate through the rows and convert each value to a float
#         for row in reader:
#             response_time_lst.append(float(row[0]))
#     return response_time_lst



######################################################################################################
# id = 4
# api = '7.quiz_submit'
# path = '/home/mihawk/SPC/sys_perf_check_tool/client_end_script/logs/resp_time'
# res_time_lst = [500.0, 507.0, 511.0, 533.0, 507.0, 526.0, 730.0, 603.0, 530.0, 671.0, 670.0, 744.0, 
#                 746.0, 999.0, 1020.9999999999999, 748.0, 741.0, 516.0, 528.0, 525.0, 693.0, 581.0, 
#                 529.0, 646.0, 687.0, 553.0, 748.0, 631.0, 535.0, 673.0, 638.0, 512.0, 519.0, 526.0, 
#                 659.0, 652.0, 567.0, 545.0, 521.0, 564.0, 649.0, 539.0, 630.0, 567.0, 594.0, 632.0, 
#                 538.0, 690.0, 608.0, 677.0, 790.0, 502.0, 606.0, 612.0, 632.0, 671.0, 609.0, 517.0, 
#                 617.0, 688.0, 669.0, 622.0, 634.0, 660.0, 562.0, 767.0, 558.0, 540.0, 733.0, 547.0, 
#                 562.0, 569.0, 698.0, 710.0, 527.0, 606.0, 660.0, 697.0, 725.0, 904.0, 885.0, 650.0, 
#                 677.0, 833.0, 839.0, 613.0, 692.0, 875.0, 894.0, 1080.0, 1069.0, 520.0, 796.0, 856.0, 
#                 884.0, 1018.0, 1042.0, 1144.0, 1131.0, 776.0, 920.0, 919.0, 988.0, 991.0, 639.0, 617.0, 
#                 1004.0, 1095.0, 1055.0, 989.0, 267.0]
# write_to_csv(id,api,path,res_time_lst)
# new_lst = read_from_csv(id,api,path)
# print(new_lst)

######################################################################################################
lst = ['2023-10-21_17-33-43','2023-10-21_17-31-02','2023-10-21_17-29-09','2023-10-21_17-23-02']
for test_id in lst:
    extract_historical_data(test_id)
    print(get_auto_test_id())
######################################################################################################

# def db_query():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("select * from test")
#     val = cursor.fetchall()
#     print(val)
#     cursor.execute("PRAGMA table_info(test)")
#     schema = cursor.fetchall()
#     print(schema)
#     conn.commit()
#     conn.close()
#     pass

# db_query()