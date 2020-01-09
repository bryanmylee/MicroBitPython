from microbit import *

CHAR_DELAY = 800

DOT_MIN = 0
DOT_MAX = 250
DASH_MIN = 250
DASH_MAX = 800

MAX_SCROLL_DELAY = 200
MIN_SCROLL_DELAY = 80

# A lookup table of morse codes and associated characters.
MORSE_CODE_LOOKUP = {# {{{
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0"
}# }}}


def get_scroll_delay(message_length):
    delay = MAX_SCROLL_DELAY - message_length * 5
    if delay < MIN_SCROLL_DELAY:
        delay = MIN_SCROLL_DELAY
    return delay


# current char code
charCodeBuff = ""
# current message
message = ""

last_button_down_time = running_time()
last_button_up_time = running_time()

while True:
    # If more time than CHAR_DELAY has passed since the last button up
    if running_time() - last_button_up_time > CHAR_DELAY and charCodeBuff != "":
        # Lookup the code, else place a space
        parsed_char = MORSE_CODE_LOOKUP.get(charCodeBuff, " ")
        # Show the parsed character for feedback
        display.show(parsed_char)
        message += parsed_char
        # Reset the char buffer
        charCodeBuff = ""

    # If the user enters the message
    if button_b.is_pressed() and message != "":
        # Handle the message
        display.scroll(message, delay=get_scroll_delay(len(message)))

        # Display a confirmation that the message was submitted
        display.show(Image.YES)
        sleep(500)
        display.clear()

        # Reset the state of the program
        charCodeBuff = ""
        message = ""

    if button_a.is_pressed():
        # If the last event was a button_up,
        # then this press is a button_down event
        if last_button_down_time <= last_button_up_time:
            last_button_down_time = running_time()
            # Display some feedback
            display.show(Image.ARROW_S)
    else:
        # If the last event was a button_down,
        # then this press is a button_up event
        if last_button_up_time < last_button_down_time:
            last_button_up_time = running_time()
            # Display some feedback
            display.show(Image.ARROW_N)

            press_duration = last_button_up_time - last_button_down_time
            print(press_duration)

            if DOT_MIN < press_duration <= DOT_MAX:
                print(". logged")
                charCodeBuff += "."
            elif DASH_MIN < press_duration <= DASH_MAX:
                print("- logged")
                charCodeBuff += "-"
