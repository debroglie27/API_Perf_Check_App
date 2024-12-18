import os
import requests
import subprocess
from math import ceil
from settings.config import TEST_SERVER_HOST


def sys_perf_check(test_id,msg="",num_user=0):
    url = TEST_SERVER_HOST+ f"sys_perf_check/{test_id}-{msg}/{num_user}/"
    requests.get(url)


def performance_test(num_user, ramp_up, duration, test_id):
    sys_perf_check(test_id, "START")

    # Calculate the user rate
    rate = ceil(num_user * ramp_up)
    
    # Use os.path.join to handle cross-platform path formatting
    perfcheck_script = os.path.join(".", "core", "perfcheck.py")
    
    # Build the locust command
    locust_cmd = [
        "locust", "-f", perfcheck_script,
        "--headless", "-u", str(num_user),
        "-r", str(rate), "-t", str(duration),
        "--csv-full-history", f"--csv={test_id}/{num_user}"
    ]
    
    # Run the locust command using subprocess
    process = subprocess.Popen(locust_cmd)
    process.wait()  # Wait for the process to finish

    sys_perf_check(test_id, "END")
