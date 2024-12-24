import os
import gevent
from gevent.event import Event
import logging
import requests
from math import ceil
from locust.env import Environment
from locust.stats import stats_printer, stats_history, StatsCSVFileWriter
from core.perfcheck import MySeqTest
from settings.config import TEST_SERVER_HOST

# Set the logging level for Locust
logging.basicConfig(level=logging.INFO)


def sys_perf_check(test_id, msg="", num_user=0):
    url = TEST_SERVER_HOST + f"sys_perf_check/{test_id}-{msg}/{num_user}/"
    requests.get(url)


def performance_test(num_user, ramp_up, duration, test_id):
    # Generate the START log in the server
    sys_perf_check(test_id, "START")

    # Calculate the user rate
    rate = ceil(num_user / ramp_up)

    # Define the directory for CSV output
    csv_output_dir = f"{test_id}"
    os.makedirs(csv_output_dir, exist_ok=True)

    # Custom CSV filenames
    stats_csv_path = os.path.join(csv_output_dir, f"{num_user}")
    history_csv_path = os.path.join(csv_output_dir, f"{num_user}")

    # Create Locust environment with the PerfCheck class
    env = Environment(user_classes=[MySeqTest])
    env.create_local_runner()

    # Define percentiles to report
    percentiles_to_report = [50, 90, 95, 99]

    # Set up CSV writers
    StatsCSVFileWriter(
        env.stats,
        base_filepath=stats_csv_path,
        percentiles_to_report=percentiles_to_report
    )
    StatsCSVFileWriter(
        env.stats,
        base_filepath=history_csv_path,
        full_history=True,
        percentiles_to_report=percentiles_to_report
    )

    # Start stats printing in the console and history tracking
    printer_greenlet = gevent.spawn(stats_printer(env.stats))

    # Set up stats history tracking
    gevent.spawn(stats_history, env.runner)

    # Start the Locust test with the specified number of users and spawn rate
    env.runner.start(user_count=num_user, spawn_rate=rate)

    # Schedule the test to stop after the specified duration
    gevent.spawn_later(duration, env.runner.quit)

    # Run the test
    env.runner.greenlet.join()

    # Forcefully kill the stats printer greenlet
    printer_greenlet.kill()

    # Generate the END log in the server
    sys_perf_check(test_id, "END")
