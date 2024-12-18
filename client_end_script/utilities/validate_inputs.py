def validate_inputs(num_users, ramp_up, duration):
    """
    Validate the inputs for the test.
    
    Args:
        num_users: The number of users (integer or string).
        ramp_up: The ramp-up time (float or string).
        duration: The test duration (integer or string).

    Returns:
        Validated num_users (int), ramp_up (float), and duration (int).
    
    Raises:
        ValueError: If any input is invalid.
    """
    try:
        num_users = int(num_users)  # Convert and validate num_users
    except ValueError:
        raise ValueError("Number of Users must be an integer.")
    
    try:
        ramp_up = float(ramp_up)  # Convert and validate ramp_up
        if not 0 <= ramp_up <= 1:
            raise ValueError("Ramp Up Rate must be a float between 0 and 1.")
    except ValueError:
        raise ValueError("Ramp Up Rate must be a float between 0 and 1.")

    try:
        duration = int(duration)  # Convert and validate duration
    except ValueError:
        raise ValueError("Duration must be an integer.")

    return num_users, ramp_up, duration