#!/bin/bash

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

echo "CSV files have been collected and permissions updated."
