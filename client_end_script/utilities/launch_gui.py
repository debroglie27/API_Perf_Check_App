import sys
from tkinter import Tk, Label, Entry, Button, Frame, messagebox


def center_window(root, width, height):
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the dimensions of the window and position it
    root.geometry(f"{width}x{height}+{x}+{y}")


def on_submit(root, num_users_entry, ramp_up_entry, delay_entries, user_inputs):
    try:
        # Collect and validate input from the GUI
        user_inputs["num_users"] = int(num_users_entry.get())
        user_inputs["ramp_up"] = float(ramp_up_entry.get())

        # Validate that ramp_up is between 0 and 1 (inclusive)
        if not (0 <= user_inputs["ramp_up"] <= 1):
            raise ValueError("Ramp up rate must be between 0 and 1.")

        # Collect delays from the delay entry fields
        user_inputs["delays"] = [int(entry.get()) for entry in delay_entries]

        # Show Info message in a messagebox
        messagebox.showinfo("Information", "Performance Test Started")

        root.destroy()  # Close the GUI
    except ValueError as e:
        # Show error message in a messagebox
        messagebox.showerror("Input Error", f"Invalid input! {e}")


def on_close(root):
    print("Application closed by the user.")
    root.destroy()  # Ensure the application ends cleanly
    sys.exit()


def launch_gui():
    # Store inputs in a dictionary for easy retrieval
    user_inputs = {"num_users": None, "ramp_up": None, "delays": [1, 1, 1, 1, 1, 1, 1]}

    # Create the GUI window
    root = Tk()
    root.title("API Perf Check Tool")

    # Set window background color
    root.configure(bg="#a0dafa")

    # Set desired window dimensions
    window_width = 620
    window_height = 675

    # Center the window
    center_window(root, window_width, window_height)

    # Bind the close event to the on_close function
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))

    # Configure the grid layout
    root.grid_columnconfigure(0, weight=1)  # Center column 0

    input_label_font = ("Arial", 18)
    delay_label_font = ("Arial", 15)
    header_font = ("Arial", 22)
    input_entry_font = ("Arial", 18)
    delay_entry_font = ("Arial", 15)
    button_font = ("Arial", 16)

    # Frame for Inputs
    inputs_frame = Frame(root, bg="#a0dafa")
    inputs_frame.grid(row=0, column=0, padx=10, pady=(55, 20), sticky="nsew")
    inputs_frame.grid_columnconfigure(0, weight=1)
    inputs_frame.grid_columnconfigure(1, weight=1)

    # Num Users Label and Entry
    Label(inputs_frame, text="Number of Users:", font=input_label_font, bg="#a0dafa").grid(row=0, column=0, padx=10, pady=(0, 10), sticky="e")
    num_users_entry = Entry(inputs_frame, font=input_entry_font, borderwidth=0, relief="flat", justify="center")
    num_users_entry.grid(row=0, column=1, padx=10, pady=(0, 10), sticky="w")

    # Ramp-Up Rate Label and Entry
    Label(inputs_frame, text="Ramp-Up Rate:", font=input_label_font, bg="#a0dafa").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    ramp_up_entry = Entry(inputs_frame, font=input_entry_font, borderwidth=0, relief="flat", justify="center")
    ramp_up_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Frame for Delays
    delays_frame = Frame(root, bg="#a0dafa")
    delays_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    delays_frame.grid_columnconfigure(0, weight=1)
    delays_frame.grid_columnconfigure(1, weight=1)

    Label(delays_frame, text="Delays", font=header_font, bg="#a0dafa").grid(row=0, column=0, padx=10, pady=(0, 15), columnspan=2)

    delay_labels = [
        "Login:", "Course List:", "Quiz List:", "Quiz Info:",
        "Quiz Download:", "Quiz Authenticate:", "Quiz Submit:"
    ]
    delay_entries = []

    for i, label_text in enumerate(delay_labels):
        Label(delays_frame, text=label_text, font=delay_label_font, bg="#a0dafa").grid(row=i+1, column=0, padx=10, pady=8, sticky="e")
        entry = Entry(delays_frame, font=delay_entry_font, borderwidth=0, relief="flat", justify="center")
        entry.grid(row=i+1, column=1, padx=10, pady=8, sticky="w")
        entry.insert(0, "1")  # Default value
        delay_entries.append(entry)

    # Submit button to validate input and close the GUI
    submit_button = Button(root, text="SUBMIT", font=button_font, padx=40, pady=10, bg="#42b52d", fg="white", borderwidth=0, highlightthickness=0, relief="flat",
                           command=lambda: on_submit(root, num_users_entry, ramp_up_entry, delay_entries, user_inputs))
    submit_button.grid(row=3, column=0, pady=(30, 10))

    root.mainloop()

    # Return user inputs after the GUI is closed
    return user_inputs["num_users"], user_inputs["ramp_up"], user_inputs["delays"]
