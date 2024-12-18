from tkinter import Tk, Label, Entry, Button

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

    # Store inputs in a dictionary for easy retrieval
    user_inputs = {"num_users": None, "ramp_up": None, "duration": None}

    # Create the GUI window
    root = Tk()
    root.title("Performance Test")

    # GUI labels and input fields
    Label(root, text="Number of Users:").grid(row=0, column=0, padx=10, pady=5)
    num_users_entry = Entry(root)
    num_users_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(root, text="Ramp-Up Time (s):").grid(row=1, column=0, padx=10, pady=5)
    ramp_up_entry = Entry(root)
    ramp_up_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(root, text="Duration (s):").grid(row=2, column=0, padx=10, pady=5)
    duration_entry = Entry(root)
    duration_entry.grid(row=2, column=1, padx=10, pady=5)

    # Submit button to validate input and close the GUI
    submit_button = Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

    # Return user inputs after the GUI is closed
    return user_inputs["num_users"], user_inputs["ramp_up"], user_inputs["duration"]
