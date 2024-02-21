from enum import Enum
import json,csv,os
import scipy.stats as stats
import numpy as np
from colorama import Fore, Style
from config import COMPARE_WITH_PREV_ENTRIES


class TestType(Enum):
    t_test=1
    mann_whitney_u_test=2

class TestMode(Enum):
    Auto=3
    t_test = TestType.t_test
    mann_whitney_u_test= TestType.mann_whitney_u_test

def t_test_result(curr_lst,old_lst):
    """
        1 - comparison not possible as old data does not exist
        2 - Performance decreased compared to prev entry
        3 - Performance improved compared to prev entry
        4 - Almost similar Performance . We can not reject the null hypothesis
    """
    if len(old_lst) == 0:
        return "1"
    if len(curr_lst) == 0:
        raise ValueError("Response time for current test not generated")
    t_stats,p_val = stats.ttest_ind(old_lst,curr_lst)
    # t_stats,p_val = stats.mannwhitneyu(old_lst,curr_lst)
    alpha = 0.01
    if p_val >=alpha:
        return "4"
    if t_stats <= 0:
        return "2"
    return "3"

def get_t_test_result(curr_lst,old_lst):
    _, p_value_var = stats.levene(curr_lst, old_lst)
    alpha = 0.05
    if p_value_var > alpha:
        # Variances are comparable, apply independent t-test
        t_stat, p_val = stats.ttest_ind(curr_lst, old_lst, equal_var=True)
        # test_type = "Independent t-test"
    else:
        # Variances are not comparable, apply Welch t-test
        t_stat, p_val = stats.ttest_ind(curr_lst, old_lst, equal_var=False)
        # test_type = "Welch t-test"
    if len(old_lst) == 0:
        return "1"
    if len(curr_lst) == 0:
        raise ValueError("Response time for current test not generated")
    # t_stats,p_val = stats.ttest_ind(old_lst,curr_lst)
    # t_stats,p_val = stats.mannwhitneyu(old_lst,curr_lst)
    if p_val >=alpha:
        return "4"
    if t_stat <= 0:
        return "2"
    return "3"

def get_mann_whitney_u_test_result(curr_lst,old_lst):
    alpha = 0.05
    u_stat, p_value_mw = stats.mannwhitneyu(curr_lst, old_lst, alternative='two-sided')
    t_stat, p_val= u_stat, p_value_mw
    test_type = "Mann-Whitney U test"
    if p_val >=alpha:
        return "4"
    return "5"


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

def generate_test_results(test_mode,db_test_id,log_path):
    headers= ["API Name","Avg. Resp Time","std deviation"]
    for val in COMPARE_WITH_PREV_ENTRIES:
        headers.append("-"+str(val)+" D")
    res = []
    res.append(headers)

    with open('APIs.json','r') as f:
        api_info = json.load(f)
    apilist=[]
    for item in api_info:
        filename=item["APIName"]
        apilist.append(filename)
    for apiname in apilist:
        api_info=[]
        api_rt_lst = read_from_csv(db_test_id,apiname,log_path) # response time
        api_mean = round(np.mean(api_rt_lst),2)
        api_std_dev = round(np.std(api_rt_lst),2)
        api_info.append(apiname)
        api_info.append(str(api_mean))
        api_info.append(str(api_std_dev))
        for val in COMPARE_WITH_PREV_ENTRIES:
            prev_id = db_test_id-val
            prev_rt_lst = read_from_csv(prev_id,apiname,log_path)
            # change the below two lines
            if test_mode == TestMode.Auto:
                alpha_to_check_normal_dis = 0.5
                _, p_value_dist1 = stats.normaltest(api_rt_lst)
                _, p_value_dist2 = stats.normaltest(prev_rt_lst)
                if p_value_dist1 > alpha_to_check_normal_dis and p_value_dist2 >alpha_to_check_normal_dis:
                    test_res = get_t_test_result(api_rt_lst,prev_rt_lst)
                    print("hit")
                else:
                    test_res = get_mann_whitney_u_test_result(api_rt_lst,prev_rt_lst)
                pass
            elif test_mode == TestMode.t_test:
                test_res = get_t_test_result(api_rt_lst,prev_rt_lst)
            elif test_mode == TestMode.mann_whitney_u_test:
                test_res = get_mann_whitney_u_test_result(api_rt_lst,prev_rt_lst)
            # t_res=t_test_result(api_rt_lst,prev_rt_lst)
            api_info.append(str(test_res))
        res.append(api_info)
    return res
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

def print_performance(code):
    if code == "1":
        print(f"{Fore.LIGHTBLACK_EX}{Style.BRIGHT}.{Style.RESET_ALL}",end='')
    elif code == "2":
        print(f"{Fore.RED}{Style.BRIGHT}-{Style.RESET_ALL}",end='')
    elif code == "3":
        print(f"{Fore.GREEN}{Style.BRIGHT}+{Style.RESET_ALL}",end='')
    elif code == "4":
        print(f"{Fore.LIGHTBLACK_EX}{Style.BRIGHT}={Style.RESET_ALL}",end='')
    elif code == "5":
        print(f"{Fore.YELLOW}{Style.BRIGHT}c{Style.RESET_ALL}",end='')


if __name__ == "__main__":

    base_dir=os.getcwd()
    log_data_dir = base_dir+"/logs/resp_time"
    test_mode = TestMode.Auto
    db_test_id = 40
    result = generate_test_results(test_mode,db_test_id,log_data_dir)
    print(result)
    print_test_results(result)
    print_performance("1")
    print_performance("2")
    print_performance("3")
    print_performance("4")
    print_performance("5")
