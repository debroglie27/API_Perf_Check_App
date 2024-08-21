#!/bin/bash

# Array of user numbers and ramp-up rates
USER_NUMBERS=(120 130 140 150)
RAMP_UP_RATE=0.1

# Run the performance script for each number of users
for num_users in "${USER_NUMBERS[@]}"; do
    echo "Performance Script running for $num_users users and $RAMP_UP_RATE ramp_up rate"
    sudo docker run --rm -p 5500:5500 -v $(pwd):/app api_perf_check_app python3 client_end_module.py -l $num_users -r $RAMP_UP_RATE
    echo "Waiting for 1 second before the next run..."
    sleep 1
done

echo "Performance Scripts Done."

# Create the destination directory
DEST_DIR="./collected_csvs"
mkdir -p $DEST_DIR

# Find and copy all CSV files from folders starting with '2024'
for dir in 2024*/; do
    if [ -d "$dir" ]; then
        csv_file="${dir}*_stats.csv"
        if [ -f $csv_file ]; then
            cp $csv_file $DEST_DIR/
            sudo chmod 777 "${DEST_DIR}/$(basename $csv_file)"
        fi
    fi
done

sudo chmod 777 "collected_csvs/"

echo "All Done."
