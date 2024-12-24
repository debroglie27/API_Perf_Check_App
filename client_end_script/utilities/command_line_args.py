import argparse

def command_line_args():
    parser = argparse.ArgumentParser(prog='./client_end_module.py', description='To monitor performance of APIs over time')
    parser.add_argument('-l',metavar="NUM_OF_USERS",required=True,type=int,help='The number of users to simulate during the performance test')
    parser.add_argument('-r',metavar="RAMP_UP_RATE",default=0.1,type=float,help='The ramp up rate for performance test (between 0 and 1)')
    parser.add_argument('-t',metavar="DURATION",default=60,type=int,help='The duration for the locust loadtest')
    args = parser.parse_args()

    return args.l, args.r, args.t