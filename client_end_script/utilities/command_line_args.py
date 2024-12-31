import argparse

def validate_ramp_up_rate(value):
    """Validate that the ramp-up rate is between 0 and 1 inclusive."""
    try:
        rate = float(value)
        if 0 <= rate <= 1:
            return rate
        else:
            raise argparse.ArgumentTypeError("Ramp up rate must be between 0 and 1 (inclusive).")
    except ValueError:
        raise argparse.ArgumentTypeError("Ramp up rate must be a valid number.")


def command_line_args():
    parser = argparse.ArgumentParser(prog='./client_end_module.py', description='To monitor performance of APIs over time')
    parser.add_argument('-l',metavar="NUM_OF_USERS",required=True,type=int,help='The number of users to simulate during the performance test')
    parser.add_argument('-r',metavar="RAMP_UP_RATE",default=0.1,type=validate_ramp_up_rate,help='The ramp up rate for performance test (between 0 and 1)')
    parser.add_argument('-d', metavar="DELAY", nargs=7, type=int, default=[1, 1, 1, 1, 1, 1, 1], help='Exactly 7 delays (space-separated), default is 1 for all')
    args = parser.parse_args()

    return args.l, args.r, args.d