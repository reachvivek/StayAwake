import pyautogui
import time
import math
import threading
from pynput import mouse, keyboard

# Disable the fail-safe (use cautiously)
pyautogui.FAILSAFE = False

radius = 50  # Distance of the jiggle movement
inactivity_limit = 15  # Time in seconds before starting to jiggle
inactive_time = 0  # Time since last interaction
stop_jiggler_event = threading.Event()  # Event to control jiggler activation
suppress_ctrl_detection = False  # Flag to suppress detection of ctrl press by jiggler
is_running = True  # Flag to control program execution

def reset_inactivity(*args):
    """Resets inactivity timer and stops jiggler if active, unless suppressed."""
    global inactive_time
    # Ignore reset if we're suppressing detection of ctrl press by jiggler
    if not suppress_ctrl_detection and stop_jiggler_event.is_set():
        inactive_time = 0  # Reset inactivity timer
        update_console("*** User activity detected! Stopping the mouse jiggler. ***")
        stop_jiggler()

def stop_jiggler():
    """Stops the jiggler and updates necessary flags."""
    global inactive_time
    inactive_time = 0  # Reset inactivity timer
    stop_jiggler_event.clear()  # Clear the event to stop jiggling
    update_console("*** Mouse jiggler has been stopped. ***")

def update_console(message):
    """Update the console with a message, overwriting the current line."""
    print(message, end='\r')

def monitor_inactivity():
    """Monitors inactivity and triggers the jiggling action when needed."""
    global inactive_time
    update_console("*** Monitoring user activity... ***")
    while is_running:  # Keep monitoring while the program is running
        time.sleep(1)
        inactive_time += 1  # Increment inactivity timer

        if inactive_time >= inactivity_limit and not stop_jiggler_event.is_set():
            update_console("*** Inactivity detected! Starting the mouse jiggler... ***")
            stop_jiggler_event.set()  # Set event to start jiggling
            threading.Thread(target=perform_jiggle).start()
        else:
            update_console(f"*** Inactive for {inactive_time} seconds... ***")

def perform_jiggle():
    """Performs jiggle action in a circular motion, including ctrl press, until stopped."""
    global suppress_ctrl_detection
    x, y = pyautogui.position()
    update_console("*** Mouse jiggler is now active. Jiggling to prevent sleep... ***")

    last_jiggle_time = time.time()  # Track the last jiggle time
    is_waiting = False  # Flag to indicate if waiting for the next jiggle

    while stop_jiggler_event.is_set() and is_running:
        current_time = time.time()
        
        # Only perform jiggle if at least 15 seconds have passed since the last jiggle
        if current_time - last_jiggle_time >= 15:
            # Move the mouse in a circular pattern
            for angle in range(0, 360, 90):
                if not stop_jiggler_event.is_set():  # Stop if the event is cleared
                    return
                new_x = x + radius * math.cos(math.radians(angle))
                new_y = y + radius * math.sin(math.radians(angle))
                pyautogui.moveTo(new_x, new_y, duration=0.1)

            # Suppress ctrl detection while the jiggler presses ctrl
            suppress_ctrl_detection = True
            pyautogui.press('ctrl')  # Simulate ctrl press
            suppress_ctrl_detection = False

            update_console("*** Ctrl key pressed to prevent system sleep... ***")
            last_jiggle_time = current_time  # Update the last jiggle time
            is_waiting = False  # Reset waiting flag
        elif not is_waiting:
            update_console("*** Waiting for 15 seconds before the next jiggle... ***")
            is_waiting = True  # Set waiting flag

        time.sleep(1)  # Short delay before checking again

    # Reset jiggler state after stopping
    stop_jiggler_event.clear()

def on_stop_key_press(key):
    """Callback to stop the program when Escape key is pressed."""
    global is_running
    if key == keyboard.Key.esc:  # Check if Escape is pressed
        stop_jiggler_event.clear()  # Ensure jiggler is stopped
        is_running = False  # Set running flag to False
        update_console("\n*** Exiting the program... ***")
        return False  # Stop the listener

# Start listeners for mouse and keyboard events
mouse_listener = mouse.Listener(on_move=reset_inactivity)
keyboard_listener = keyboard.Listener(on_press=reset_inactivity)

mouse_listener.start()
keyboard_listener.start()

# Start monitoring inactivity in a separate thread
inactivity_monitor_thread = threading.Thread(target=monitor_inactivity, daemon=True)
inactivity_monitor_thread.start()

# Start listening for the stop key (Escape key)
keyboard_listener_stop = keyboard.Listener(on_press=on_stop_key_press)
keyboard_listener_stop.start()

# Keep the main thread alive
inactivity_monitor_thread.join()
