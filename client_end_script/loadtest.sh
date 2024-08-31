#!/bin/bash

# Array of user numbers and ramp-up rates
USER_NUMBERS=(10 20 30 40 50 60 70 80 90 100)
RAMP_UP_RATE=0.1

# Run the performance script for each number of users
for num_users in "${USER_NUMBERS[@]}"; do
    echo "Performance Script running for $num_users users and $RAMP_UP_RATE ramp_up rate"
    sudo docker run --rm -p 5500:5500 -v $(pwd):/app api_perf_check_app python3 client_end_module.py -l $num_users -r $RAMP_UP_RATE
    echo "Waiting for 1 second before the next run..."
    sleep 1
done

echo "Performance Scripts Done."


# Loop through all folders starting with "2024" in the current directory
for folder in 2024*/; do
  # Check if it is a directory
  if [ -d "$folder" ]; then
    echo "Found directory: $folder"

    # Loop through subfolders starting with "uwsgi" within the "2024" folder
    for uwsgi_folder in "$folder"uwsgi*/; do
      # Check if it is a directory
      if [ -d "$uwsgi_folder" ]; then
        echo "Found uwsgi folder: $uwsgi_folder"

        # Apply chmod 777 to the uwsgi folder
        sudo chmod -R 777 "$uwsgi_folder"

        echo "Permissions changed to 777 for $uwsgi_folder"
      else
        echo "No uwsgi folder found in $folder"
      fi
    done
  else
    echo "$folder is not a directory or does not exist."
  fi
done

sudo rm -rf *.tar.gz

echo "All Done."
