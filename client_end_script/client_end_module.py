from client_end_script_helper import (
    command_line_args_apc,
    generate_test_id,
    create_test_directory,
    performance_test,
    get_server_logs,
    extract_historical_data,
    constructor_script
)

if __name__ == '__main__':
    number_of_users, ramp_up= command_line_args_apc()
    test_id = generate_test_id()
    constructor_script()
    create_test_directory(test_id)
    performance_test(number_of_users,ramp_up, test_id)
    get_server_logs(test_id)
    extract_historical_data(test_id)
