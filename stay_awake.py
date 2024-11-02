import pyautogui
import time
import math

# Define the radius of the jiggle movement
radius = 10
interval = 5  # seconds

try:
    while True:
        # Get current mouse position
        x, y = pyautogui.position()
        
        # Move the mouse in a circular pattern
        for angle in range(0, 360, 45):
            new_x = x + radius * math.cos(math.radians(angle))
            new_y = y + radius * math.sin(math.radians(angle))
            pyautogui.moveTo(new_x, new_y, duration=0.1)
        
        # Wait before next jiggle
        time.sleep(interval)

except KeyboardInterrupt:
    print("Mouse jiggling stopped.")
