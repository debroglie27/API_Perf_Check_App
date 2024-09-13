#!/bin/bash

# Array of user numbers and ramp-up rates
USER_NUMBERS=(150 140 130 120 110 100 90 80 70 60 50 40 30 20 10)
RAMP_UP_RATE=0.1
DURATIONS=(30 30 30 30 30 25 25 25 25 25 21 20 20 20 20)

# Run the performance script for each number of users
for i in "${!USER_NUMBERS[@]}"; do
    num_users=${USER_NUMBERS[$i]}
    duration=${DURATIONS[$i]}
    
    echo "Performance Script running for $num_users users, $RAMP_UP_RATE ramp-up rate, and $duration seconds duration"
    python3 client_end_module.py -l $num_users -r $RAMP_UP_RATE -t $duration
    rm *.tar.gz

    echo "Waiting for 1 second before the next run..."
    sleep 1
done

echo "All Done."
