#!/bin/bash

# Activate the virtual environment
source myenv/bin/activate

# Array of user numbers and ramp-up rates
USER_NUMBERS=(60 50 40 30 20 10)
RAMP_UP_RATE=0.1

# Run the performance script for each number of users
for i in "${!USER_NUMBERS[@]}"; do
    num_users=${USER_NUMBERS[$i]}
    
    echo "Performance Script running for $num_users users, $RAMP_UP_RATE ramp-up rate"
    python3 main.py -l $num_users -r $RAMP_UP_RATE

    echo "Waiting for 1 second before the next run..."
    sleep 1
done

echo "All Done."
