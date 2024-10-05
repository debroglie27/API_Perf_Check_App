from initial_script import initial_setup
from client_end_script_helper import (
    command_line_args_apc,
    generate_test_id,
    create_test_directory,
    performance_test,
    get_server_logs,
    extract_data,
)


if __name__ == '__main__':
    num_users, ramp_up, duration = command_line_args_apc()
    test_id = generate_test_id()
    initial_setup()
    create_test_directory(test_id)
    performance_test(num_users, ramp_up, duration, test_id)
    get_server_logs(test_id)
    extract_data(test_id)
