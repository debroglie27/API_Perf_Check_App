import csv
import time

def write_locust_stats(env, file_path):
    """Manually write Locust stats to a CSV file."""

    print(f"Writing locust stats to {file_path}")
    stats = env.stats
    timestamp = int(time.time())

    # Define CSV Columns
    columns = [
        "Timestamp",
        "Type",
        "Name",
        "Requests/s",
        "Failures/s",
        "Total Request Count",
        "Total Failure Count",
        "Median Response Time",
        "Average Response Time",
        "Min Response Time",
        "Max Response Time",
        "Average Content Size",
    ]

    # Open CSV File and Write Stats
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)

        # Write Total Stats
        total = stats.total
        writer.writerow([
            timestamp,
            "Total",
            "All Requests",
            f"{total.current_rps:.2f}",
            f"{total.current_fail_per_sec:.2f}",
            total.num_requests,
            total.num_failures,
            total.median_response_time,
            total.avg_response_time,
            total.min_response_time or 0,
            total.max_response_time,
            total.avg_content_length,
        ])

        # Write Per-Endpoint Stats
        for _, entry in stats.entries.items():
            writer.writerow([
                timestamp,
                entry.method or "N/A",
                entry.name,
                f"{entry.current_rps:.2f}",
                f"{entry.current_fail_per_sec:.2f}",
                entry.num_requests,
                entry.num_failures,
                entry.median_response_time,
                entry.avg_response_time,
                entry.min_response_time or 0,
                entry.max_response_time,
                entry.avg_content_length,
            ])

    print(f"Locust Stats written successfully to {file_path}")