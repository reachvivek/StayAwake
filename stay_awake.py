import pyautogui
import time
import math
import threading
from pynput import mouse, keyboard

# Disable the fail-safe (use cautiously)
pyautogui.FAILSAFE = False

radius = 10         # Distance of the jiggle movement
inactivity_limit = 30  # Time in seconds to wait before starting to jiggle
start_time = time.time()  # Record the start time
inactive_time = 0  # Time since last interaction
jiggler_active = False  # Flag to indicate if jiggler is currently active
trigger_count = 0  # Counter for the number of times jiggler was triggered

def print_elapsed_time(start_time):
    """Function to print the elapsed time in HH:MM:SS format."""
    while True:
        elapsed_time = time.time() - start_time
        
        # Convert elapsed time to hours, minutes, and seconds
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        # Format the time as HH:MM:SS
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(f"Running Time: {formatted_time}", end='\r')  # Print the timer on the same line
        time.sleep(1)  # Update every second

def on_activity(x, y):
    """Callback for mouse movement to reset inactive timer."""
    global inactive_time, jiggler_active
    inactive_time = 0  # Reset inactivity timer
    if jiggler_active:  # If jiggler is active, set it to inactive
        jiggler_active = False
        print("\n*** Activity detected! Stopping the mouse jiggler. ***")

def on_key_press(key):
    """Callback for key press to reset inactive timer."""
    global inactive_time, jiggler_active
    inactive_time = 0  # Reset inactivity timer
    if jiggler_active:  # If jiggler is active, set it to inactive
        jiggler_active = False
        print("\n*** Activity detected! Stopping the mouse jiggler. ***")

def mouse_jiggler():
    """Function to jiggle the mouse after inactivity period."""
    global inactive_time, jiggler_active, trigger_count
    while True:
        time.sleep(1)  # Check every second
        inactive_time += 1  # Increment inactivity timer

        if inactive_time >= inactivity_limit and not jiggler_active:
            # Alert user about inactivity
            print("\n*** Inactivity detected! Starting the mouse jiggler to stay awake... ***")
            jiggler_active = True  # Set the jiggler active flag
            trigger_count += 1  # Increment the trigger count

            # Get current mouse position
            x, y = pyautogui.position()

            # Move the mouse in a circular pattern
            for angle in range(0, 360, 45):
                new_x = x + radius * math.cos(math.radians(angle))
                new_y = y + radius * math.sin(math.radians(angle))
                pyautogui.moveTo(new_x, new_y, duration=0.1)

            # Display the number of times the jiggler has been triggered
            print(f"*** Mouse jiggler triggered to stay awake {trigger_count} times so far. ***")

            inactive_time = 0  # Reset inactivity timer after jiggling

# Start the timer thread
timer_thread = threading.Thread(target=print_elapsed_time, args=(start_time,), daemon=True)
timer_thread.start()

# Start mouse and keyboard listeners
mouse_listener = mouse.Listener(on_move=on_activity)
keyboard_listener = keyboard.Listener(on_press=on_key_press)

mouse_listener.start()
keyboard_listener.start()

# Start the jiggler function
mouse_jiggler()
