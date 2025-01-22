import sys
from gevent import monkey
monkey.patch_all()

from core.run_test import run_test

from utilities.get_args_gui import get_args_gui
from utilities.write_task_wait_times import write_task_wait_times
from utilities.get_args_command_line import get_args_command_line


def main():
    try:
        if len(sys.argv) == 1:
            # No command-line arguments provided; launch GUI
            num_users, ramp_up, delays = get_args_gui()
        else:
            # Extract command-line arguments
            num_users, ramp_up, delays = get_args_command_line()

        # Write the task delays to a json file
        write_task_wait_times(delays)

        # Run the test
        run_test(num_users, ramp_up)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
    
