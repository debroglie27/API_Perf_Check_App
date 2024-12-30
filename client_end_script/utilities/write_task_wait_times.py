import os
import json


def write_task_wait_times(delays):
    """
    Writes the delays into a JSON file with task names as keys.

    Parameters:
        delays (list[int]): List of 7 delays in the order: login, course_list, 
                            quiz_list, quiz_info, quiz_download, 
                            quiz_authenticate, quiz_submit.
    """
    if len(delays) != 7:
        raise ValueError("Exactly 7 delays must be provided.")
    
    # Map delays to corresponding tasks
    task_delays = {
        "login": delays[0],
        "course_list": delays[1],
        "quiz_list": delays[2],
        "quiz_info": delays[3],
        "quiz_download": delays[4],
        "quiz_authenticate": delays[5],
        "quiz_submit": delays[6],
    }

    current_dir = os.getcwd()
    output_file = os.path.join(current_dir, "settings", "task_wait_times.json")
    
    # Write the dictionary to the JSON file
    with open(output_file, "w") as f:
        json.dump(task_delays, f, indent=4)
    
    print(f"Task wait times written to {output_file}")