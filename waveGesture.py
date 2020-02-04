from microbit import *

BUFFER_SIZE = 10
SENSITIVITY = 0.3

last_light_levels = []
def update_light_levels(new_level):
    global last_light_levels
    last_light_levels.append(new_level)

    if len(last_light_levels) > BUFFER_SIZE:
        last_light_levels = last_light_levels[1:]


def get_average_gradient():
    if len(last_light_levels) == 1: return 0.0

    # Assuming l = a + bt, where l is the light, and t is time
    # We assume the data is evenly spaced on the time axis
    # Therefore the average t will be half of len(last_light_levels)
    tbar = (len(last_light_levels) - 1) / 2
    lbar = sum(last_light_levels) / len(last_light_levels)

    # Gradient formula
    num = sum([t * l for t, l in enumerate(last_light_levels)]) - len(last_light_levels) * tbar * lbar
    den = sum([t**2 for t in range(len(last_light_levels))]) - len(last_light_levels) * tbar**2

    return num / den

"""
For debugging: generates a simple line plot of the gradient.
"""
def print_plot(value):
    value *= 10
    center = 30
    print(" " * (center + int(value)) + "|")

last_show_time = running_time()
while True:
    # Dark to bright of 0 - 255
    curr_light = display.read_light_level()
    update_light_levels(curr_light)

    # If the brightness dips suddenly, we can assume that something waved over the sensors
    if get_average_gradient() < -SENSITIVITY:
        display.show(Image.SURPRISED)
        last_show_time = running_time()

    if running_time() - last_show_time > 2000:
        display.clear()

    sleep(100)


