import tkinter as tk
from PIL import ImageTk, Image
import unittest
import unittest.mock as mock
import main


def get_env():
    main.first = first_name_input.get()
    main.last = last_name_input.get()
    main.email = email_input.get()
    main.password = password_input.get()

    if dev_selected.get():
        main.selected_env = "dev"
        # current environment will use the same URL for all environments since only one environment available
        current_environment = "https://magento.softwaretestingboard.com/"
        print(current_environment)
        return current_environment
    elif prod_selected.get():
        main.selected_env = "prod"
        current_environment = "https://magento.softwaretestingboard.com/"
        print(current_environment)
        return current_environment
    elif stage_selected.get():
        main.selected_env = "stage"
        current_environment = "https://magento.softwaretestingboard.com/"
        print(current_environment)
        return current_environment


def update_button_state():
    if dev_selected.get() or prod_selected.get() or stage_selected.get():
        button.config(state="normal")  # Enable the "Run Tests" button
    else:
        button.config(state="disabled")  # Disable the "Run Tests" button


# Declare my_image as a global variable
my_image = None

# Set the width of the input boxes
input_width = 40

# Create a new Tkinter window
window = tk.Tk()
window.geometry("400x300")
window.title("Marcial - Automation Project")


def create_label(text, row, column):
    tk.Label(window, text=text).grid(row=row, column=column)


def create_input_box(row, column):
    input_box = tk.Entry(window, width=input_width, bg="dark gray")
    input_box.grid(row=row, column=column)
    return input_box


# Create labels and input boxes for each input field
create_label("First Name:", 1, 0)
first_name_input = create_input_box(1, 1)

create_label("Last Name:", 2, 0)
last_name_input = create_input_box(2, 1)

create_label("Email:", 3, 0)
email_input = create_input_box(3, 1)

create_label("Password:", 4, 0)
password_input = create_input_box(4, 1)

# Set the show attribute of the password input box to hide the text
password_input.configure(show="*")

create_label("Environment:", 5, 0)

# Variables to track the selected environments
dev_selected = tk.BooleanVar()
stage_selected = tk.BooleanVar()
prod_selected = tk.BooleanVar()


# Create the checkboxes for environment selection
dev_checkbox = tk.Checkbutton(window, text="Dev", variable=dev_selected)
dev_checkbox.grid(row=6, column=1, sticky="w")

stage_checkbox = tk.Checkbutton(window, text="Stage", variable=stage_selected)
stage_checkbox.grid(row=7, column=1, sticky="w")

prod_checkbox = tk.Checkbutton(window, text="Prod", variable=prod_selected)
prod_checkbox.grid(row=8, column=1, sticky="w")


@mock.patch('tkinter.Tk')
def run_tests(mock_tk):
    from tests import Tests
    global current_env
    current_env = get_env()

    # Retrieve the values entered by the user in the input fields
    user_first = first_name_input.get()
    user_last = last_name_input.get()
    user_email = email_input.get()  # Get the value from the email input field

    # Print the input values to the console
    print(f"First name: {user_first}")
    print(f"Last name: {user_last}")
    print(f"Email: {user_email}")

    # Initialize the Test Suite
    suite = unittest.TestSuite()

    # Locate all test cases within Tests class and add them
    suite.addTest(unittest.makeSuite(Tests))

    # Run the tests
    test_runner = unittest.TextTestRunner()
    test_runner.run(suite)


# Create a button to run the tests
button = tk.Button(window, text="Run Tests", command=run_tests)
button.grid(row=9, columnspan=2, pady=10)

# Configure the checkboxes to call the update_button_state function when clicked
dev_selected.trace("w", lambda *args: update_button_state())
prod_selected.trace("w", lambda *args: update_button_state())
stage_selected.trace("w", lambda *args: update_button_state())

# Disable the "Run Tests" button initially
button.config(state="disabled")

# Calculate the center position of the window
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Adjust column weights to center the UI
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Set the window position and center the UI
window.geometry(f"+{x}+{y}")

window.mainloop()
