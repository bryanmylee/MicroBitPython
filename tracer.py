from microbit import *

ACCELERATION = 0.001
MIN_POS = 0
MAX_POS = 4

# Creates an image with a single pixel at the x and y coord
def get_image(x, y):
    print(x, y)
    pixels = ""
    for i in range(5):
        for j in range(5):
            if j == x and i == y:
                pixels += '9'
                continue
            pixels += '0'
        pixels += ':'
    return Image(pixels)


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

    display.show(get_image(int(xpos), int(ypos)))

