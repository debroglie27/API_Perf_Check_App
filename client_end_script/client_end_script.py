#!/usr/bin/python3
from client_end_script_helper import (
    command_line_args_apc,
    generate_test_id,
    create_test_directory,
    performance_test,
    get_server_logs,
    extract_data,
    extract_historical_data,
    showGraph,
    constructor_script
)
from plotcpu import(
    plotcpu,
)
from maingui import(
    showgui,
)

if __name__ == '__main__':
    number_of_users, run_time = command_line_args_apc()
    test_id = generate_test_id()
    constructor_script()
    create_test_directory(test_id)
    performance_test(number_of_users, number_of_users, 1, run_time, test_id)
    get_server_logs(test_id)
    extract_historical_data(test_id)
    # extract_data(test_id)
    # showGraph(test_id)
    # plotcpu(test_id)
    # showgui(test_id)
    
