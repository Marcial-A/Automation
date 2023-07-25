from workspace import dev_selected, prod_selected, stage_selected, button
selected_env = None
first = None
last = None
email = None
password = None


def update_button_state():
    if dev_selected.get() or prod_selected.get() or stage_selected.get():
        button.config(state="normal")  # Enable the "Run Tests" button
    else:
        button.config(state="disabled")  # Disable the "Run Tests" button


if __name__ == "__main__":
    # Configure the checkboxes to call the update_button_state function when clicked
    dev_selected.trace("w", lambda *args: update_button_state())
    prod_selected.trace("w", lambda *args: update_button_state())
    stage_selected.trace("w", lambda *args: update_button_state())

    # Call update_button_state() once to set the initial button state
    update_button_state()
