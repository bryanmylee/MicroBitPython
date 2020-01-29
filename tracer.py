from microbit import *

ACCELERATION = 0.001
MIN_POS = 0
MAX_POS = 4
TRACE_FADE_DELAY = 1000

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = running_time()

    def get_coord(self):
        return self.x, self.y


# Stores Pixel
trace = []

# Updates the trace
def update_trace(xpos, ypos):
    global trace

    if len(trace) == 0: 
        trace.append(Pixel(xpos, ypos))
    elif trace[0].get_coord() != (xpos, ypos):
        trace = [Pixel(xpos, ypos)] + trace

    trace = [p for p in trace if running_time() - p.time < TRACE_FADE_DELAY]


def get_image():
    global trace

    px_str = "00000:00000:00000:00000:00000"

    curr_time = running_time()
    for i, pixel in enumerate(trace):
        index = pixel.y * 6 + pixel.x
        life = curr_time - pixel.time

        px_str = px_str[:index] + str(get_brightness(life)) + px_str[index+1:]

    return Image(px_str)

# Returns 1...9 based on how long a pixel has been alive
def get_brightness(life):
    if life >= TRACE_FADE_DELAY:
        return 0

    return int(9 * (1 - life / TRACE_FADE_DELAY))


def get_bound_pos(x, y):
    if x < MIN_POS: x = MIN_POS
    if x > MAX_POS: x = MAX_POS
    if y < MIN_POS: y = MIN_POS
    if y > MAX_POS: y = MAX_POS
    return x, y


xpos, ypos = 2., 2.
while True:
    # Returns values -1000...1000
    dx, dy, dz = accelerometer.get_values()

    # Scale the acceleration down
    dx *= ACCELERATION
    dy *= ACCELERATION

    # Displace the position
    xpos += dx
    ypos += dy

    # Bound x and y
    xpos, ypos = get_bound_pos(xpos, ypos)
    update_trace(int(xpos), int(ypos))

    display.show(get_image())

