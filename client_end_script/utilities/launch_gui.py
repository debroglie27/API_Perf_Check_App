import sys
from tkinter import Tk, Label, Entry, Button


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
    window_width = 500
    window_height = 310

    # Center the window
    center_window(root, window_width, window_height)

    # Bind the close event to the on_close function
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Configure the grid layout
    root.grid_columnconfigure(0, weight=1)  # Center column 0
    root.grid_columnconfigure(1, weight=1)  # Center column 1

    label_font = ("Arial", 15)
    entry_font = ("Arial", 15)
    button_font = ("Arial", 15)

    # GUI labels and input fields
    Label(root, text="Number of Users:", font=label_font, bg="#a0dafa").grid(row=0, column=0, padx=10, pady=(45, 10), sticky="e")
    num_users_entry = Entry(root, font=entry_font, borderwidth=0, relief="flat")
    num_users_entry.grid(row=0, column=1, padx=10, pady=(45, 10), sticky="w")

    Label(root, text="Ramp-Up Rate:", font=label_font, bg="#a0dafa").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    ramp_up_entry = Entry(root, font=entry_font, borderwidth=0, relief="flat")
    ramp_up_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    Label(root, text="Duration (s):", font=label_font, bg="#a0dafa").grid(row=2, column=0, padx=10, pady=(10, 40), sticky="e")
    duration_entry = Entry(root, font=entry_font, borderwidth=0, relief="flat")
    duration_entry.grid(row=2, column=1, padx=10, pady=(10, 40), sticky="w")

    # Submit button to validate input and close the GUI
    submit_button = Button(root, text="SUBMIT", font=button_font, padx=40, pady=10, bg="#42b52d", fg="white", borderwidth=0, highlightthickness=0, relief="flat", command=on_submit)
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

    # Return user inputs after the GUI is closed
    return user_inputs["num_users"], user_inputs["ramp_up"], user_inputs["duration"]
