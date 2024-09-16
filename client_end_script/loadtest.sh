#!/bin/bash

# Activate the virtual environment
source myenv/bin/activate

# Array of user numbers and ramp-up rates
USER_NUMBERS=(50 45 40 35 30 25 20 15 10 5)
RAMP_UP_RATE=0.1
DURATIONS=(95 90 85 80 60 50 40 35 25 20)

# Run the performance script for each number of users
for i in "${!USER_NUMBERS[@]}"; do
    num_users=${USER_NUMBERS[$i]}
    duration=${DURATIONS[$i]}
    
    echo "Performance Script running for $num_users users, $RAMP_UP_RATE ramp-up rate, and $duration seconds duration"
    python3 client_end_module.py -l $num_users -r $RAMP_UP_RATE -t $duration

    echo "Waiting for 1 second before the next run..."
    sleep 1
done

echo "All Done."
