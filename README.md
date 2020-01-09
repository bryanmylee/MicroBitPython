# micro:bit Projects

Here are a collection of interesting programs I've built during my embedded systems course.

We are provided with a micro:bit as part of our lab, so what better way to familiarise myself with the hardware than to use it lots and built things I find interesting?

## What is micro:bit?

micro:bit is an ARM-based embedded system that is commonly used in education.

The micro:bit contains a notable amount of hardware features, including multiple radios, buttons, LEDs that double as light sensors, accelerometers, and a compass to name a few. That makes it perfect for quickly testing out ideas for small embedded systems.

## MicroPython

The code here is written for MicroPython, a slimmed-down implementation of Python 3 for embedded systems.

To compile and run this on a micro:bit, we can use the [uflash](https://uflash.readthedocs.io/en/latest/) utility to automatically compile and flash the appropriate code onto the system.

Code is translated into the Intel HEX format, then appended onto the firmware of the micro:bit, and gets parsed by the system upon startup.

## Projects available

### morseParser

Morse code is received on button A, and the message is scrolled through the display when button B is pressed.

This program provides feedback for all button presses, and confirms every character that is entered.

To adjust the timing of dots and dashes, as well as the character-parsing delay, modify the settings in the script and flash it onto your micro:bit


