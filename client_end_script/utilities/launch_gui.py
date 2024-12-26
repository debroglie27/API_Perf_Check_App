import sys
from tkinter import Tk, Label, Entry, Button, Frame


def center_window(root, width, height):
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the dimensions of the window and position it
    root.geometry(f"{width}x{height}+{x}+{y}")


def launch_gui():
    def on_submit():
        try:
            # Collect and validate input from the GUI
            user_inputs["num_users"] = int(num_users_entry.get())
            user_inputs["ramp_up"] = int(ramp_up_entry.get())
            user_inputs["duration"] = int(duration_entry.get())
            root.destroy()  # Close the GUI
        except ValueError:
            print("Invalid input! Please enter valid integers.")

    def on_close():
        print("Application closed by the user.")
        root.destroy()  # Ensure the application ends cleanly
        sys.exit()

    # Store inputs in a dictionary for easy retrieval
    user_inputs = {"num_users": None, "ramp_up": None, "duration": None}

    # Create the GUI window
    root = Tk()
    root.title("API Perf Check Tool")

    # Set window background color
    root.configure(bg="#a0dafa")

    # Set desired window dimensions
    window_width = 650
    window_height = 700

    # Center the window
    center_window(root, window_width, window_height)

    # Bind the close event to the on_close function
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Configure the grid layout
    root.grid_columnconfigure(0, weight=1)  # Center column 0

    label_font = ("Arial", 15)
    header_font = ("Arial", 20)
    entry_font = ("Arial", 15)
    button_font = ("Arial", 15)

    # Frame for Delays
    inputs_frame = Frame(root, bg="#a0dafa")
    inputs_frame.grid(row=0, column=0, padx=10, pady=(50, 10), sticky="nsew")

    inputs_frame.grid_columnconfigure(0, weight=1)
    inputs_frame.grid_columnconfigure(1, weight=1)

    # Num Users Label and Entry
    Label(inputs_frame, text="Number of Users:", font=label_font, bg="#a0dafa").grid(row=0, column=0, padx=10, pady=(0, 10), sticky="e")
    num_users_entry = Entry(inputs_frame, font=entry_font, borderwidth=0, relief="flat")
    num_users_entry.grid(row=0, column=1, padx=10, pady=(0, 10), sticky="w")

    Label(inputs_frame, text="Ramp-Up Rate:", font=label_font, bg="#a0dafa").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    ramp_up_entry = Entry(inputs_frame, font=entry_font, borderwidth=0, relief="flat")
    ramp_up_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    Label(inputs_frame, text="Duration:", font=label_font, bg="#a0dafa").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    duration_entry = Entry(inputs_frame, font=entry_font, borderwidth=0, relief="flat")
    duration_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Delay Label
    Label(root, text="Delays", font=header_font, bg="#a0dafa").grid(row=1, column=0, pady=(20, 0), sticky="nsew")

    # Frame for Delays
    delays_frame = Frame(root, bg="#a0dafa")
    delays_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    delays_frame.grid_columnconfigure(0, weight=1)
    delays_frame.grid_columnconfigure(1, weight=1)
    delays_frame.grid_columnconfigure(2, weight=1)

    Label(delays_frame, text="Login", font=label_font, bg="#a0dafa").grid(row=0, column=0, padx=10, pady=8, sticky="e")
    delay_login_entry = Entry(delays_frame, font=entry_font, borderwidth=0, relief="flat")
    delay_login_entry.grid(row=0, column=1, padx=10, pady=8)
    Label(delays_frame, text="Course List", font=label_font, bg="#a0dafa").grid(row=0, column=2, padx=10, pady=8, sticky="w")

    Label(delays_frame, text="Course List", font=label_font, bg="#a0dafa").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    delay_course_list_entry = Entry(delays_frame, font=entry_font, borderwidth=0, relief="flat")
    delay_course_list_entry.grid(row=1, column=1, padx=10, pady=8)
    Label(delays_frame, text="Quiz List", font=label_font, bg="#a0dafa").grid(row=1, column=2, padx=10, pady=8, sticky="w")

    Label(delays_frame, text="Quiz List", font=label_font, bg="#a0dafa").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    delay_quiz_list_entry = Entry(delays_frame, font=entry_font, borderwidth=0, relief="flat")
    delay_quiz_list_entry.grid(row=2, column=1, padx=10, pady=8)
    Label(delays_frame, text="Quiz Info", font=label_font, bg="#a0dafa").grid(row=2, column=2, padx=10, pady=8, sticky="w")

    Label(delays_frame, text="Quiz Info", font=label_font, bg="#a0dafa").grid(row=3, column=0, padx=10, pady=8, sticky="e")
    delay_quiz_info_entry = Entry(delays_frame, font=entry_font, borderwidth=0, relief="flat")
    delay_quiz_info_entry.grid(row=3, column=1, padx=10, pady=8)
    Label(delays_frame, text="Quiz Download", font=label_font, bg="#a0dafa").grid(row=3, column=2, padx=10, pady=8, sticky="w")

    Label(delays_frame, text="Quiz Download", font=label_font, bg="#a0dafa").grid(row=4, column=0, padx=10, pady=8, sticky="e")
    delay_quiz_download_entry = Entry(delays_frame, font=entry_font, borderwidth=0, relief="flat")
    delay_quiz_download_entry.grid(row=4, column=1, padx=10, pady=8)
    Label(delays_frame, text="Quiz Authenticate", font=label_font, bg="#a0dafa").grid(row=4, column=2, padx=10, pady=8, sticky="w")

    Label(delays_frame, text="Quiz Authenticate", font=label_font, bg="#a0dafa").grid(row=5, column=0, padx=10, pady=8, sticky="e")
    delay_quiz_authenticate_entry = Entry(delays_frame, font=entry_font, borderwidth=0, relief="flat")
    delay_quiz_authenticate_entry.grid(row=5, column=1, padx=10, pady=8)
    Label(delays_frame, text="Quiz Submit", font=label_font, bg="#a0dafa").grid(row=5, column=2, padx=10, pady=8, sticky="w")

    Label(delays_frame, text="Quiz Submit", font=label_font, bg="#a0dafa").grid(row=6, column=0, padx=10, pady=8, sticky="e")
    delay_quiz_submit_entry = Entry(delays_frame, font=entry_font, borderwidth=0, relief="flat")
    delay_quiz_submit_entry.grid(row=6, column=1, padx=10, pady=8)
    Label(delays_frame, text="Finish", font=label_font, bg="#a0dafa").grid(row=6, column=2, padx=10, pady=8, sticky="w")


    # Submit button to validate input and close the GUI
    submit_button = Button(root, text="SUBMIT", font=button_font, padx=40, pady=10, bg="#42b52d", fg="white", borderwidth=0, highlightthickness=0, relief="flat", command=on_submit)
    submit_button.grid(row=3, column=0, pady=(30, 10))

    root.mainloop()

    # Return user inputs after the GUI is closed
    return user_inputs["num_users"], user_inputs["ramp_up"], user_inputs["duration"]
