from microbit import *

# Scale of acceleration on the head pixel
ACCELERATION = 0.001
# How long each pixel lasts on screen (in ms)
TRACE_FADE_DELAY = 1000


class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = running_time()

    def get_coord(self):
        return self.x, self.y


# A list of Pixel
trace = []
def update_trace(xpos, ypos):
    global trace

    if len(trace) == 0:
        trace = [Pixel(xpos, ypos)]
        return

    # Only update the trace if there is a change in the head position
    if trace[0].get_coord() != (xpos, ypos):
        trace = [Pixel(xpos, ypos)] + trace

    # We want to always keep the first Pixel, therefore we only run our filter on trace[1:]
    trace = [trace[0]] + [p for p in trace[1:] if running_time() - p.time < TRACE_FADE_DELAY]


def get_image():
    global trace

    px_str = "00000:00000:00000:00000:00000"

    for i, pixel in enumerate(trace):
        px_str = insert_px(px_str, pixel)

    if len(trace) != 0:
        px_str = insert_px(px_str, trace[0], brightness=9)

    return Image(px_str)


# Returns a new pixel string given a new Pixel
# If no brightness is specified, the it is calculated from pixel lifespan
def insert_px(px_str, pixel, brightness=None):
    index = pixel.y * 6 + pixel.x
    if brightness == None:
        life = running_time() - pixel.time
        return px_str[:index] + str(get_brightness(life)) + px_str[index+1:]
    return px_str[:index] + str(brightness) + px_str[index+1:]


# Returns 1...9 based on how long a pixel has been alive
def get_brightness(life):
    if life >= TRACE_FADE_DELAY:
        return 0

    return int(9 * (1 - life / TRACE_FADE_DELAY))


MIN_POS = 0
MAX_POS = 4
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

