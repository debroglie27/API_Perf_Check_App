import os
import gevent
import logging
import requests
from math import ceil
from locust.env import Environment
from locust.stats import stats_printer, stats_history

from core.locust_script import MySeqTest
from settings.config import TEST_SERVER_HOST
from utilities.shared_resources import all_users_complete
from utilities.write_locust_stats import write_locust_stats

# Set the logging level for Locust
logging.basicConfig(level=logging.INFO)


# Used to generate the START and END log at the server
def sys_perf_check(test_id, msg="", num_user=0):
    url = TEST_SERVER_HOST + f"sys_perf_check/{test_id}-{msg}/{num_user}/"
    requests.get(url)


# Wait for users to finish
def wait_for_users_to_finish(env, num_user):
    """
    Waits for all users to finish their tasks.
    Stops the Locust runner when the semaphore value indicates all users are done.

    :param env: Locust Environment instance.
    :param num_user: Total number of users to wait for.
    """
    while True:
        current_value = all_users_complete.value
        print(f"Waiting for users. Current semaphore value: {current_value}")
        if current_value >= num_user:
            print("All users completed. Stopping Locust.")
            break

        gevent.sleep(2)

    env.runner.quit()


def performance_test(num_user, ramp_up, test_id):
    # Generate the START log in the server
    sys_perf_check(test_id, "START")

    # Calculate the user rate
    rate = ceil(num_user * ramp_up)

    # Define the directory for CSV output of locust stats
    csv_output_dir = f"{test_id}"
    os.makedirs(csv_output_dir, exist_ok=True)

    stats_csv_path = os.path.join(csv_output_dir, f"{num_user}_stats.csv")

    # Create Locust Environment
    env = Environment(user_classes=[MySeqTest])
    env.create_local_runner()

    # Start Locust Test
    printer_greenlet = gevent.spawn(stats_printer(env.stats))

    # Set up stats history tracking
    gevent.spawn(stats_history, env.runner)

    # Set up a thread to track user completion
    gevent.spawn(wait_for_users_to_finish, env, num_user)

    # Start the Locust test with the specified number of users and spawn rate
    env.runner.start(user_count=num_user, spawn_rate=rate)

    # Locust Test Completes
    env.runner.greenlet.join()

    # Forcefully kill the stats printer greenlet
    printer_greenlet.kill()

    # Manually write stats after test completion
    write_locust_stats(env, stats_csv_path)

    # Generate the END log in the server
    sys_perf_check(test_id, "END")
