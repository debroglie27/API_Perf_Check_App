import sys
from gevent import monkey
monkey.patch_all()

from core.run_test import run_test

from utilities.launch_gui import launch_gui
from utilities.validate_inputs import validate_inputs
from utilities.command_line_args import command_line_args


def main():
    # print(len(sys.argv)) # Number of Arguments
    try:
        if len(sys.argv) != 7 and len(sys.argv) != 1:
            raise ValueError("Invalid number of arguments. Provide either 0 or 3 arguments.")

        if len(sys.argv) == 7:
            # Extract command-line arguments
            num_users, ramp_up, duration = command_line_args()
        else:
            # No command-line arguments provided; launch GUI
            num_users, ramp_up, duration = launch_gui()

        # Validate inputs
        num_users, ramp_up, duration = validate_inputs(num_users, ramp_up, duration)

        # Run the test
        run_test(num_users, ramp_up, duration)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
    
