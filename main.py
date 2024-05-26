import threading
import time
import tkinter as tk
import random

# Define a class for the typing speed GUI application
class TypeSpeedGUI:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Typing Speed Application")
        self.root.geometry("800x600")

        # Try to read text samples from a file, handle error if file not found
        try:
            with open("text.txt", "r") as file:
                self.texts = file.read().split("\n")
        except FileNotFoundError:
            self.texts = ["File not found. Please make sure 'text.txt' is present."]

        # Display a random text sample from the file
        self.sample_label = tk.Label(self.root, text=random.choice(self.texts), font="Helvetica", wraplength=750,
                                     justify="left")
        self.sample_label.grid(row=0, column=0, padx=5, pady=5)

        # Create a frame to hold the input entry and labels
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=1, column=0, padx=5, pady=5)

        # Entry widget for user to type into
        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyPress>", self.start_typing)  # Bind key press event to start_typing method

        # Label to display typing speed in WPM
        self.speed_label = tk.Label(self.frame, text="Speed:\n 0.00 WPM", font="Helvetica", wraplength=750,
                                    justify="left")
        self.speed_label.grid(row=0, column=0, padx=5, pady=5)

        # Label to display the remaining time
        self.timer_label = tk.Label(self.frame, text="Time left: 60s", font="Helvetica", wraplength=750, justify="left")
        self.timer_label.grid(row=0, column=1, padx=5, pady=5)

        # Reset button to reset the typing test
        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # Initialize variables for the timer and running state
        self.counter = 60
        self.running = False

        # Start the main event loop
        self.root.mainloop()

    def start_typing(self, event):
        # Start the typing test timer when the user starts typing
        if not self.running:
            if event.keycode not in [16, 17, 18]:  # Ignore Shift, Ctrl, Alt keys
                self.running = True
                self.start_time = time.time()
                self.end_time = self.start_time + 60  # Set end time to 60 seconds from start time
                t = threading.Thread(target=self.time_thread)
                t.start()  # Start the timer thread

        # Get the sample text and the user's input text
        sample_text = self.sample_label.cget('text')
        input_text = self.input_entry.get()

        # Check if the input text matches the beginning of the sample text
        if sample_text.startswith(input_text):
            self.input_entry.config(fg="black")
        else:
            self.input_entry.config(fg="red")

        # If the entire sample text is typed correctly, stop the timer
        if input_text == sample_text:
            self.running = False
            self.input_entry.config(fg="green")

    def reset(self):
        # Reset the typing test to its initial state
        self.running = False
        self.counter = 60
        new_text = random.choice(self.texts)
        self.sample_label.config(text=new_text)
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(fg="black")
        self.speed_label.config(text="Speed:\n 0.00 WPM")
        self.timer_label.config(text="Time left: 60s")

    def time_thread(self):
        # Timer thread to update the time left and typing speed
        while self.running and self.counter > 0:
            time_left = self.end_time - time.time()
            if time_left <= 0:
                self.running = False
                time_left = 0

            self.counter = time_left
            self.timer_label.config(text=f"Time left: {int(time_left)}s")

            # Calculate words per minute (WPM)
            words = len(self.input_entry.get().split())
            elapsed_time = 60 - self.counter
            wpm = (words / elapsed_time) * 60 if elapsed_time > 0 else 0
            self.speed_label.config(text="Speed:\n {:.2f} WPM".format(wpm))

            time.sleep(0.1)

        # If timer stops, change text color to green
        if not self.running:
            self.input_entry.config(fg="green")

# Run the typing speed GUI application
if __name__ == "__main__":
    TypeSpeedGUI()
