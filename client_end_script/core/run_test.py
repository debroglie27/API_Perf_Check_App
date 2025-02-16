# from core.initial_user import initial_user
from core.organize_logs import organize_logs
from core.initial_script import initial_setup
from core.get_server_logs import get_server_logs
from core.performance_test import performance_test
from core.extract_response_times import extract_response_times

from utilities.generate_test_id import generate_test_id


def run_test(num_users, ramp_up):
    test_id = generate_test_id()
    initial_setup()
    # initial_user()
    performance_test(num_users, ramp_up, test_id)
    get_server_logs(test_id)
    organize_logs(test_id)
    extract_response_times(test_id)
