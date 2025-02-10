import os
import csv
import json
import numpy as np
# from colorama import Fore, Style
import scipy.stats as stats
from scipy.stats import mannwhitneyu


def read_from_csv(test_id, prefix, api_name):
    base_path = os.getcwd()
    csv_filename = prefix + "_response_times.csv"
    csv_file_path = os.path.join(base_path, test_id, csv_filename)

    response_times = []

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)  # Automatically uses the first row as column names

        if api_name not in reader.fieldnames:
            raise ValueError(f"API name '{api_name}' not found in CSV headers")

        for row in reader:
            response_times.append(int(row[api_name]))  # Convert to float for numerical operations

    return response_times


def normality_test(curr_l):
    # print("Normality check")
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


def t_test_result(curr_lst,old_lst):
    """
        1 - comparison not possible as old data does not exist
        2 - Performance decreased compared to prev entry
        3 - Performance improved compared to prev entry
        4 - Almost similar Performance . We can not reject the null hypothesis
    """
    # print("t test used")
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
    # print("u test used")
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


def generate_t_test_results(test_id1, test_id2):
    res = []
    
    with open('settings/APIs.json','r') as f:
        api_info = json.load(f)

    for api in api_info:
        api_rt_lst_1 = read_from_csv(test_id1, "inner-nginx", api['name']) # response time
        api_rt_lst_2 = read_from_csv(test_id2, "inner-nginx", api['name']) # response time

        normal_1 = normality_test(api_rt_lst_1)
        normal_2 = normality_test(api_rt_lst_2)
        if (normal_1 and normal_2):
            t_res = t_test_result(api_rt_lst_1, api_rt_lst_2)
        else:
            t_res = man_u_test_result(api_rt_lst_1, api_rt_lst_2)

        res.append([api['name'], str(t_res)])
    
    return res


if __name__ == "__main__":
    test_id_1 = "2025-01-13_19-40-16"
    test_id_2 = "2025-01-02_11-12-59"

    result = generate_t_test_results(test_id_1,test_id_2)

    print(result)
