from core.extract_data import extract_data
from core.initial_script import initial_setup
from core.get_server_logs import get_server_logs
from core.performance_test import performance_test

from utilities.generate_test_id import generate_test_id
from utilities.create_test_directory import create_test_directory

def run_test(num_users, ramp_up, duration):
    test_id = generate_test_id()
    initial_setup()
    create_test_directory(test_id)
    performance_test(num_users, ramp_up, duration, test_id)
    get_server_logs(test_id)
    extract_data(test_id)