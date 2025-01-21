import sys
import time

import urllib.request

class Microbit:
    """Microbit Class includes the control of the outputs and inputs
    present on the micro:bit."""

    # Test requests to find the devices connected
    base_request_out = "http://127.0.0.1:30061/hummingbird/out"
    base_request_in = "http://127.0.0.1:30061/hummingbird/in"
    stopall = "http://127.0.0.1:30061/hummingbird/out/stopall"

    symbolvalue = None

    # ---------------------------------------------------------------------------------
    # UTILITY FUNCTIONS
    # ---------------------------------------------------------------------------------
    def __init__(self, device='A'):
        """Called when the class is initialized."""

        # Check if the letter of the device is valid, exit otherwise
        if ('ABC'.find(device) != -1):
            self.device_s_no = device
            # Check if the device is connected and if it is a micro:bit
            if not self.isConnectionValid():
                self.stopAll()
                sys.exit()

            if not self.isMicrobit():        # it isn't a micro:bit
                print("Error: Device " + str(self.device_s_no) + " is not a micro:bit")
                self.stopAll()
                sys.exit()
            self.symbolvalue = [0]*25
        else:
            print("Error: Device must be A, B, or C.")
            self.stopAll()
            sys.exit()

    def isConnectionValid(self):
        """This function tests a connection by attempting to read whether or
        not the micro:bit is shaking. Return true if the connection is good
        and false otherwise."""

        http_request = self.base_request_in + "/" + "orientation" + "/" + "Shake" + "/" + str(self.device_s_no)
        try:
            response_request = urllib.request.urlopen(http_request)
        except (ConnectionError, urllib.error.URLError):
            print("DEBUG: caught the connection valid exception")
            print(CONNECTION_SERVER_CLOSED)
            return False
        response = response_request.read().decode('utf-8')

        if (response == "Not Connected"):
            print("Error: Device " + str(self.device_s_no) + " is not connected")
            return False
        return True

    def isMicrobit(self):
        """This function determines whether or not the device is a micro:bit."""

        http_request = self.base_request_in + "/isMicrobit/static/" + str(self.device_s_no)
        response = self._send_httprequest(http_request)

        # Old versions of BlueBird Connector don't support this request
        if (response != ""):
            return (response == 'true')
        else:
            # Try to read sensor 4. The value will be 255 for a micro:bit (there is no sensor 4)
            # And some other value for the Hummingbird
            http_request = self.base_request_in + "/" + "sensor" + "/4/" + str(self.device_s_no)
            response = self._send_httprequest(http_request)

            return (response == "255")

    def clampParametersToBounds(self, input, inputMin, inputMax):
        """This function checks whether an input parameter is within the
        given bounds. If not, it prints a warning and returns a value of the
        input parameter that is within the required range. Otherwise, it
        just returns the initial value."""

        if ((input < inputMin) or (input > inputMax)):
            print("Warning: Please choose a parameter between " + str(inputMin) + " and " + str(inputMax))
            return max(inputMin, min(input, inputMax))
        else:
            return input

    def process_display(self, value):
        """Convert a string of 1's and 0's into true and false."""

        new_str = ""
        for letter in value:
            if (letter == 0):
                new_str += "false/"
            else:  # All nonzero values become true
                new_str += "true/"

        # Remove the last character in a string
        new_str = new_str[:len(new_str)-1]
        return new_str

    @staticmethod
    def __constrainToInt(number):
        """Utility function to ensure number is an integer. Will round and cast to int
        (with warning) if necessary."""

        if not isinstance(number, int):
            oldNumber = number
            number = int(round(number))
            print("Warning: Parameter must be an integer. Using " + str(number) + " instead of " + str(oldNumber) + ".")

        return number

    # ---------------------------------------------------------------------
    # OUTPUTS MICRO BIT
    # ---------------------------------------------------------------------
    def setDisplay(self, LEDlist):
        """Set Display of the LED Array on microbit with the given input LED
        list of 0's and 1's."""

        # Check if LED_string is valid to be printed on the display
        # Check if the length of the array to form a symbol not equal than 25
        if (len(LEDlist) != 25):
            print("Error: setDisplay() requires a list of length 25")
            return             # if the array is the wrong length, don't want to do anything else

        # Check if all the characters entered are valid
        for index in range(0, len(LEDlist)):
            LEDlist[index] = self.clampParametersToBounds(LEDlist[index], 0, 1)

        # Reset the display status
        self.symbolvalue = LEDlist

        # Convert the LED_list to  an appropriate value which the server can understand
        LED_string = self.process_display(LEDlist)
        # Send the http request
        response = self.send_httprequest_micro("symbol", LED_string)
        return response

    def print(self, message):
        """Print the characters on the LED screen."""

        # Warn the user about any special characters - we can mostly only print English characters and digits
        for letter in message:
            if not (((letter >= 'a') and (letter <= 'z')) or ((letter >= 'A') and (letter <= 'Z')) or
                    ((letter >= '0') and (letter <= '9')) or (letter == ' ')):
                print("Warning: Many special characters cannot be printed on the LED display")

        # Need to replace spaces with %20
        message = message.replace(' ', '%20')

        # Empty out the internal representation of the display, since it will be blank when the print ends
        self.symbolvalue = [0]*25

        # Send the http request
        response = self.send_httprequest_micro("print", message)
        return response

    def setPoint(self, x, y, value):
        """Choose a certain LED on the LED Array and switch it on or off.
        The value specified should be 1 for on, 0 for off."""

        # Check if x, y and value are valid
        x = self.clampParametersToBounds(x, 1, 5)
        y = self.clampParametersToBounds(y, 1, 5)
        value = self.clampParametersToBounds(value, 0, 1)

        # Calculate which LED should be selected
        index = (x - 1) * 5 + (y - 1)

        # Update the state of the LED displayf
        self.symbolvalue[index] = value

        # Convert the display status to  an appropriate value which the server can understand
        outputString = self.process_display(self.symbolvalue)

        # Send the http request
        response = self.send_httprequest_micro("symbol", outputString)
        return response

    def playNote(self, note, beats):
        """Make the buzzer play a note for certain number of beats. Note is the midi
        note number and should be specified as an integer from 32 to 135. Beats can be
        any number from 0 to 16. One beat corresponds to one second."""

        # Check that both parameters are within the required bounds
        note = self.clampParametersToBounds(note, 32, 135)
        beats = self.clampParametersToBounds(beats, 0, 16)

        note = self.__constrainToInt(note)
        beats = int(beats * (60000 / TEMPO))

        # Send HTTP request
        # response = self.__send_httprequest_out("playnote", note, beats)
        http_request = self.base_request_out + "/playnote/" + str(note) + "/" + str(beats) + "/" + str(self.device_s_no)
        response = self._send_httprequest(http_request)
        return response

    # -----------------------------------------------------------------------------
    # INPUTS MICROBIT
    # -----------------------------------------------------------------------------
    def _getXYZvalues(self, sensor, intResult):
        """Return the X, Y, and Z values of the given sensor."""

        dimension = ['X', 'Y', 'Z']
        values = []

        for i in range(0, 3):
            # Send HTTP request
            response = self.send_httprequest_micro_in(sensor, dimension[i])
            if intResult:
                values.append(int(response))
            else:
                values.append(round(float(response), 3))

        return (values[0], values[1], values[2])

    def getAcceleration(self):
        """Gives the acceleration of X,Y,Z in m/sec2."""

        return self._getXYZvalues("Accelerometer", False)

    def getCompass(self):
        """Returns values 0-359 indicating the orentation of the Earth's
        magnetic field."""

        # Send HTTP request
        response = self.send_httprequest_micro_in("Compass", None)
        compass_heading = int(response)
        return compass_heading

    def getMagnetometer(self):
        """Return the values of X,Y,Z of a magnetommeter."""

        return self._getXYZvalues("Magnetometer", True)

    def getButton(self, button):
        """Return the status of the button asked. Specify button 'A', 'B', or
        'Logo'. Logo available for V2 micro:bit only."""

        button = button.upper()
        # Check if the button A and button B are represented in a valid manner
        if ((button != 'A') and (button != 'B') and (button != 'LOGO')):
            print("Error: Button must be A, B, or Logo.")
            sys.exit()
        # Send HTTP request
        response = self.send_httprequest_micro_in("button", button)
        # Convert to boolean form
        if (response == "true"):
            button_value = True
        elif (response == "false"):
            button_value = False
        else:
            print("Error in getButton: " + response)
            sys.exit()

        return button_value

    def getSound(self):
        """Return the current sound level as an integer between 1 and 100.
        Available for V2 micro:bit only."""

        response = self.send_httprequest_micro_in("V2sensor", "Sound")

        try:
            value = int(response)
        except (ConnectionError, urllib.error.URLError):
            print("Error in getSound: " + response)
            sys.exit()

        return value

    def getTemperature(self):
        """Return the current temperature as an integer in degrees Celcius.
        Available for V2 micro:bit only."""

        response = self.send_httprequest_micro_in("V2sensor", "Temperature")

        try:
            value = int(response)
        except (ConnectionError, urllib.error.URLError):
            print("Error in getTemperature: " + response)
            sys.exit()

        return value

    def isShaking(self):
        """Return true if the device is shaking, false otherwise."""

        # Send HTTP request
        response = self.send_httprequest_micro_in("Shake", None)
        if (response == "true"):  # convert to boolean
            shake = True
        else:
            shake = False

        return shake

    def getOrientation(self):
        """Return the orentation of the micro:bit. Options include:
        "Screen up", "Screen down", "Tilt left", "Tilt right", "Logo up",
        "Logo down", and "In between"."""

        orientations = ["Screen%20Up", "Screen%20Down", "Tilt%20Left", "Tilt%20Right", "Logo%20Up", "Logo%20Down"]
        orientation_result = ["Screen up", "Screen down", "Tilt left", "Tilt right", "Logo up", "Logo down"]

        # Check for orientation of each device and if true return that state
        for targetOrientation in orientations:
            response = self.send_httprequest_micro_in(targetOrientation, None)
            if (response == "true"):
                return orientation_result[orientations.index(targetOrientation)]

        # If we are in a state in which none of the above seven states are true
        return "In between"

    def stopAll(self):
        """Stop all device outputs (ie. Servos, LEDs, LED Array, Motors, etc.)."""

        time.sleep(0.1)         # Hack to give stopAll() time to act before the end of a program
        response = self.send_httprequest_stopAll()
        self.symbolvalue = [0]*25
        return response

    # -------------------------------------------------------------------------
    # SEND HTTP REQUESTS
    # -------------------------------------------------------------------------
    def _send_httprequest(self, http_request):
        """Send an HTTP request and return the result."""
        try:
            response_request = urllib.request.urlopen(http_request)
        except (ConnectionError, urllib.error.URLError):
            print(CONNECTION_SERVER_CLOSED)
            sys.exit()

        response = response_request.read().decode('utf-8')
        if (response == "Not Connected"):
            print(NO_CONNECTION)
            sys.exit()

        time.sleep(0.01)        # Hack to prevent http requests from overloading the BlueBird Connector
        return response

    def send_httprequest_micro(self, peri, value):
        """Utility function to arrange and send the http request for microbit output functions."""

        # Print command
        if (peri == "print"):
            http_request = self.base_request_out + "/" + peri + "/" + str(value) + "/" + str(self.device_s_no)
        elif (peri == "symbol"):
            http_request = self.base_request_out + "/" + peri + "/" + str(self.device_s_no) + "/" + str(value)
        try:
            response_request = urllib.request.urlopen(http_request)
            if (response_request.read() == b'200'):
                response = 1
            else:
                response = 0
        except (ConnectionError, urllib.error.URLError):
            print(CONNECTION_SERVER_CLOSED)
            sys.exit()
        time.sleep(0.01)        # Hack to prevent http requests from overloading the BlueBird Connector
        return response

    def send_httprequest_micro_in(self, peri, value):
        """Utility function to arrange and send the http request for microbit input functions."""

        if (peri == "Accelerometer"):
            http_request = self.base_request_in + "/" + peri + "/" + str(value) + "/" + str(self.device_s_no)
        elif (peri == "Compass"):
            http_request = self.base_request_in + "/" + peri + "/" + str(self.device_s_no)
        elif (peri == "Magnetometer"):
            http_request = self.base_request_in + "/" + peri + "/" + str(value) + "/" + str(self.device_s_no)
        elif (peri == "button"):
            http_request = self.base_request_in + "/" + peri + "/" + str(value) + "/" + str(self.device_s_no)
        elif (peri == "Shake"):
            http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" + str(self.device_s_no)
        elif (peri == "Screen%20Up"):
            http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" + str(self.device_s_no)
        elif (peri == "Screen%20Down"):
            http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" + str(self.device_s_no)
        elif (peri == "Tilt%20Right"):
            http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" + str(self.device_s_no)
        elif (peri == "Tilt%20Left"):
            http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" + str(self.device_s_no)
        elif (peri == "Logo%20Up"):
            http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" + str(self.device_s_no)
        elif (peri == "Logo%20Down"):
            http_request = self.base_request_in + "/" + "orientation" + "/" + peri + "/" + str(self.device_s_no)
        else:
            http_request = self.base_request_in + "/" + peri + "/" + str(value) + "/" + str(self.device_s_no)

        try:
            response_request = urllib.request.urlopen(http_request)
        except (ConnectionError, urllib.error.URLError):
            print(CONNECTION_SERVER_CLOSED)
            sys.exit()
        response = response_request.read().decode('utf-8')
        if (response == "Not Connected"):
            print(NO_CONNECTION)
            sys.exit()
        time.sleep(0.01)        # Hack to prevent http requests from overloading the BlueBird Connector
        return response

    def send_httprequest_stopAll(self):
        """Send HTTP request for hummingbird bit output."""

        # Combine diffrenet strings to form a HTTP request
        http_request = self.stopall + "/" + str(self.device_s_no)
        try:
            response_request = urllib.request.urlopen(http_request)
        except (ConnectionError, urllib.error.URLError):
            print(CONNECTION_SERVER_CLOSED)
            sys.exit()
        if (response_request.read() == b'200'):
            response = 1
        else:
            response = 0
        time.sleep(0.01)        # Hack to prevent http requests from overloading the BlueBird Connector
        return response

    # Microbit Aliases
    acceleration = getAcceleration
    button = getButton
    compass = getCompass
    display = setDisplay
    is_connection_valid = isConnectionValid
    is_microbit = isMicrobit
    is_shaking = isShaking
    magnetometer = getMagnetometer
    orientation = getOrientation
    play_note = playNote
    point = setPoint
    sound = getSound
    stop_all = stopAll
    temperature = getTemperature

    # END class Microbit

