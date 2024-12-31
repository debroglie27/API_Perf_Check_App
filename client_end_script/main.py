import sys
from gevent import monkey
monkey.patch_all()

from core.run_test import run_test

from utilities.launch_gui import launch_gui
from utilities.write_task_wait_times import write_task_wait_times
from utilities.command_line_args import command_line_args


def main():
    try:
        if len(sys.argv) == 1:
            # No command-line arguments provided; launch GUI
            num_users, ramp_up, delays = launch_gui()
        else:
            # Extract command-line arguments
            num_users, ramp_up, delays = command_line_args()

        # Write the task delays to the task_wait_delays.json
        write_task_wait_times(delays)

        # Run the test
        run_test(num_users, ramp_up)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
    
