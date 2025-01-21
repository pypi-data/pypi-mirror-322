import sys
import time

import urllib.request

from birdbrain_microbit import Microbit

class Hummingbird(Microbit):
    """Hummingbird Bit Class includes the control of the outputs and inputs
        present on the Hummingbird Bit."""

    # -------------------------------------------------------------------------
    # UTILITY FUNCTIONS
    # -------------------------------------------------------------------------
    def __init__(self, device='A'):
        """Class initializer. Specify device letter A, B or C."""

        # Check if the length of the array to form a symbol is greater than 25"""
        if ('ABC'.find(device) != -1):
            self.device_s_no = device
            # Check if device is connected and is a hummingbird
            if not self.isConnectionValid():
                self.stopAll()
                sys.exit()
            if not self.isHummingbird():
                print("Error: Device " + str(self.device_s_no) + " is not a Hummingbird")
                self.stopAll()
                sys.exit()
            self.symbolvalue = [0]*25
        else:
            self.stopAll()
            sys.exit()

    def isHummingbird(self):
        """This function determines whether or not the device is a Hummingbird."""

        http_request = self.base_request_in + "/isHummingbird/static/" + str(self.device_s_no)
        response = self._send_httprequest(http_request)

        # Old versions of BlueBird Connector don't support this request
        if (response != ""):
            return (response == 'true')
        else:
            # Try to read sensor 4. The value will be 255 for a micro:bit (there is no sensor 4)
            # And some other value for the Hummingbird
            http_request = self.base_request_in + "/" + "sensor" + "/4/" + str(self.device_s_no)
            response = self._send_httprequest(http_request)

            return (response != "255")

    def isPortValid(self, port, portMax):
        """This function checks whether a port is within the given bounds.
        It returns a boolean value that is either true or false and prints
        an error if necessary."""

        if ((port < 1) or (port > portMax)):
            print("Error: Please choose a port value between 1 and " + str(portMax))
            return False
        else:
            return True

    def calculate_LED(self, intensity):
        """ Utility function to covert LED from 0-100 to 0-255."""

        intensity_c = int((intensity * 255) / 100)

        return intensity_c

    def calculate_RGB(self, r_intensity, g_intensity, b_intensity):
        """Utility function to covert RGB LED from 0-100 to 0-255."""

        r_intensity_c = int((r_intensity * 255) / 100)
        g_intensity_c = int((g_intensity * 255) / 100)
        b_intensity_c = int((b_intensity * 255) / 100)

        return (r_intensity_c, g_intensity_c, b_intensity_c)

    def calculate_servo_p(self, servo_value):
        """Utility function to covert Servo from 0-180 to 0-255."""

        servo_value_c = int((servo_value * 254) / 180)

        return servo_value_c

    def calculate_servo_r(self, servo_value):
        """Utility function to covert Servo from -100 - 100 to 0-255."""

        # If the vlaues are above the limits fix the instensity to maximum value,
        # if less than the minimum value fix the intensity to minimum value
        if ((servo_value > -10) and (servo_value < 10)):
            servo_value_c = 255
        else:
            servo_value_c = int((servo_value * 23 / 100) + 122)
        return servo_value_c

    # -------------------------------------------------------------------------
    # HUMMINGBIRD BIT OUTPUT
    # -------------------------------------------------------------------------
    def setLED(self, port, intensity):
        """Set LED  of a certain port requested to a valid intensity."""

        # Early return if we can't execute the command because the port is invalid
        if not self.isPortValid(port, 3):
            return

        # Check the intensity value lies with in the range of LED limits
        intensity = self.clampParametersToBounds(intensity, 0, 100)

        # Change the range from 0-100 to 0-255
        intensity_c = self.calculate_LED(intensity)
        # Send HTTP request
        response = self.send_httprequest("led", port, intensity_c)
        return response

    def setTriLED(self, port, redIntensity, greenIntensity, blueIntensity):
        """Set TriLED  of a certain port requested to a valid intensity."""

        # Early return if we can't execute the command because the port is invalid
        if not self.isPortValid(port, 2):
            return

        # Check the intensity value lies with in the range of RGB LED limits
        red = self.clampParametersToBounds(redIntensity, 0, 100)
        green = self.clampParametersToBounds(greenIntensity, 0, 100)
        blue = self.clampParametersToBounds(blueIntensity, 0, 100)

        # Change the range from 0-100 to 0-255
        (r_intensity_c, g_intensity_c, b_intensity_c) = self.calculate_RGB(red, green, blue)
        # Send HTTP request
        response = self.send_httprequest("triled", port, str(r_intensity_c) + "/" + str(g_intensity_c) + "/" + str(b_intensity_c))
        return response

    def setPositionServo(self, port, angle):
        """Set Position servo of a certain port requested to a valid angle."""

        # Early return if we can't execute the command because the port is invalid
        if not self.isPortValid(port, 4):
            return

        # Check the angle lies within servo limits
        angle = self.clampParametersToBounds(angle, 0, 180)

        angle_c = self.calculate_servo_p(angle)
        # Send HTTP request
        response = self.send_httprequest("servo", port, angle_c)
        return response

    def setRotationServo(self, port, speed):
        """Set Rotation servo of a certain port requested to a valid speed."""

        # Early return if we can't execute the command because the port is invalid
        if not self.isPortValid(port, 4):
            return

        # Check the speed lies within servo limits
        speed = self.clampParametersToBounds(speed, -100, 100)

        speed_c = self.calculate_servo_r(speed)
        # Send HTTP request
        response = self.send_httprequest("rotation", port, speed_c)
        return response

    # -------------------------------------------------------------------------
    # HUMMINGBIRD BIT INPUT
    # -------------------------------------------------------------------------
    def getSensor(self, port):
        """Read the value of the sensor attached to a certain port.
        If the port is not valid, it returns -1."""

        # Early return if we can't execute the command because the port is invalid
        if not self.isPortValid(port, 3):
            return -1

        response = self.send_httprequest_in("sensor", port)
        return response

    def getLight(self, port):
        """Read the value of the light sensor attached to a certain port."""

        response = self.getSensor(port)
        light_value = int(response * LIGHT_FACTOR)
        return light_value

    def getSound(self, port):
        """Read the value of the sound sensor attached to a certain port."""

        if port == "microbit" or port == "micro:bit" or port == "Microbit":
            return Microbit.getSound(self)

        response = self.getSensor(port)
        sound_value = int(response * SOUND_FACTOR)
        return sound_value

    def getDistance(self, port):
        """Read the value of the distance sensor attached to a certain port."""

        response = self.getSensor(port)
        distance_value = int(response * DISTANCE_FACTOR)
        return distance_value

    def getDial(self, port):
        """Read the value of the dial attached to a certain port."""

        response = self.getSensor(port)
        dial_value = int(response * DIAL_FACTOR)
        if (dial_value > 100):
            dial_value = 100
        return dial_value

    def getVoltage(self, port):
        """Read the value of  the dial attached to a certain port."""

        response = self.getSensor(port)
        voltage_value = response * VOLTAGE_FACTOR
        return voltage_value

    # -------------------------------------------------------------------------
    # SEND HTTP REQUESTS
    # -------------------------------------------------------------------------
    def send_httprequest_in(self, peri, port):
        """Send HTTP requests for Hummingbird bit inputs."""

        # Combine different strings to form an HTTP request
        http_request = self.base_request_in + "/" + peri + "/" + str(port) + "/" + str(self.device_s_no)
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
        return int(response)

    def send_httprequest(self, peri, port, value):
        """Send HTTP request for Hummingbird bit output"""

        # Combine different strings to form an HTTP request
        http_request = self.base_request_out + "/" + peri + "/" + str(port) + "/" + str(value) + "/" + str(self.device_s_no)
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

    # Hummingbird Aliases
    dial = getDial
    distance = getDistance
    is_hummingbird = isHummingbird
    is_port_valid = isPortValid
    led = setLED
    light = getLight
    position_servo = setPositionServo
    rotation_servo = setRotationServo
    sensor = getSensor
    sound = getSound
    # stop_all = stopAll
    # temperature = getTemperature
    tri_led = setTriLED
    voltage = getVoltage

    # END class Hummingbird

