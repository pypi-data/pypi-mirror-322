# --------------------------------------------------------------
# Author                  Raghunath J, revised by Bambi Brewer
#                         and Kristina Lauwers
# Last Edit Date          11/20/2019
# Description             This python file contains Microbit,
# Hummingbird, and Finch classes.
# The Microbit class controls a micro:bit via bluetooth. It
# includes methods to print on the micro:bit LED array or set
# those LEDs individually. It also contains methods to read the
# values of the micro:bit accelerometer and magnetometer.
# The Hummingbird class extends the Microbit class to incorporate
# functions to control the inputs and outputs of the Hummingbird
# Bit. It includes methods to set the values of motors and LEDs,
# as well as methods to read the values of the sensors.
# The Finch class also extends the Microbit class. This class
# similarly includes function to control the inputs and outputs
# of the Finch robot.
# --------------------------------------------------------------
import sys
import time

import urllib.request

from birdbrain_microbit import Microbit
from birdbrain_hummingbird import Hummingbird
from birdbrain_finch import Finch

# --------------------------------------------------------------
# Constants

CHAR_FLASH_TIME = 0.3  # Character Flash time

# Error strings
CONNECTION_SERVER_CLOSED = "Error: Request to device failed"
NO_CONNECTION = "Error: The device is not connected"

# Calculations after receveing the raw values for Hummingbird
DISTANCE_FACTOR = 117/100
SOUND_FACTOR = 200/255
DIAL_FACTOR = 100/230
LIGHT_FACTOR = 100/255
VOLTAGE_FACTOR = 3.3/255

# Scaling factors for Finch
BATTERY_FACTOR = 0.0406

TEMPO = 60




