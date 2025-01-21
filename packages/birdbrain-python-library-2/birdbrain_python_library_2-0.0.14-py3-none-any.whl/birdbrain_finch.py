import sys
import time

import urllib.request

from birdbrain_microbit import Microbit

class Finch(Microbit):
    """The Finch class includes the control of the outputs and inputs present
    in the Finch robot. When creating an instance, specify which robot by the
    device letter used in the BlueBirdConnector device list (A, B, or C)."""

    def __init__(self, device='A'):
        """Class initializer. """

        if ('ABC'.find(device) != -1):  # check for valid device letter
            self.device_s_no = device

            if not self.isConnectionValid():
                self.__exit("Error: Invalid Connection")

            if not self.__isFinch():
                self.__exit("Error: Device " + str(self.device_s_no) + " is not a Finch")

            self.symbolvalue = [0]*25

        else:
            self.__exit("Error: Device must be A, B, or C.")

    # Finch Utility Functions
    def __exit(self, msg):
        """Print error, shutdown robot, and exit python"""

        print(msg)
        self.stopAll()
        sys.exit()

    def __isFinch(self):
        """Determine whether or not the device is a Finch"""

        http_request = self.base_request_in + "/isFinch/static/" + str(self.device_s_no)
        response = self._send_httprequest(http_request)

        return (response == 'true')

    @staticmethod
    def __calculate_RGB(r_intensity, g_intensity, b_intensity):
        """Utility function to covert RGB LED from 0-100 to 0-255"""

        r_intensity_c = int((r_intensity * 255) / 100)
        g_intensity_c = int((g_intensity * 255) / 100)
        b_intensity_c = int((b_intensity * 255) / 100)

        return (r_intensity_c, g_intensity_c, b_intensity_c)

    @staticmethod
    def __formatRightLeft(direction):
        """Utility function to format a selection of right or left for a backend request."""

        if direction == "R" or direction == "r" or direction == "Right" or direction == "right":
            return "Right"
        elif direction == "L" or direction == "l" or direction == "Left" or direction == "left":
            return "Left"
        else:
            print("Error: Please specify either 'R' or 'L' direction.")
            return None

    @staticmethod
    def __formatForwardBackward(direction):
        """Utility function to format a selection of forward or backward for a backend request."""

        if direction == "F" or direction == "f" or direction == "Forward" or direction == "forward":
            return "Forward"
        elif direction == "B" or direction == "b" or direction == "Backward" or direction == "backward":
            return "Backward"
        else:
            print("Error: Please specify either 'F' or 'B' direction.")
            return None

    def __send_httprequest_in(self, peri, port):
        """Send HTTP requests for Finch inputs.
        Combine strings to form a HTTP input request.
        Send the request and return the result as a string."""

        http_request = self.base_request_in + "/" + peri + "/" + str(port) + "/" + str(self.device_s_no)
        response = self._send_httprequest(http_request)
        return response

    def __send_httprequest_out(self, arg1, arg2, arg3):
        """Send HTTP request for Finch output.
        Combine strings to form a HTTP output request.
        Send the request and return 1 if successful, 0 otherwise."""

        requestString = "/" + arg1 + "/"
        if not (arg2 is None):
            requestString = requestString + str(arg2) + "/"
        if not (arg3 is None):
            requestString = requestString + str(arg3) + "/"

        http_request = self.base_request_out + requestString + str(self.device_s_no)
        response = self._send_httprequest(http_request)

        if (response == "200"):
            return 1
        else:
            return 0

    def __send_httprequest_move(self, arg1, arg2, arg3, arg4):
        """Send HTTP request to move the Finch.
        Combine strings to form a HTTP output request.
        Send the request and return 1 if successful, 0 otherwise."""

        requestString = "/" + arg1 + "/" + str(self.device_s_no) + "/" + str(arg2) + "/"
        if not (arg3 is None):
            requestString = requestString + str(arg3) + "/"
        if not (arg4 is None):
            requestString = requestString + str(arg4) + "/"

        http_request = self.base_request_out + requestString
        response = self._send_httprequest(http_request)

        if (response == "200"):
            return 1
        else:
            return 0

    # Finch Output
    def __setTriLED(self, port, redIntensity, greenIntensity, blueIntensity):
        """Set TriLED(s) on the Finch.
        Port 1 is the beak. Ports 2 to 5 are tail. Specify port "all" to set the whole tail."""

        # Early return if we can't execute the command because the port is invalid
        if ((not port == "all") and ((port < 1) or (port > 5))):
            return 0

        # Check the intensity value lies with in the range of RGB LED limits
        red = self.clampParametersToBounds(redIntensity, 0, 100)
        green = self.clampParametersToBounds(greenIntensity, 0, 100)
        blue = self.clampParametersToBounds(blueIntensity, 0, 100)

        # Change the range from 0-100 to 0-255
        (red_c, green_c, blue_c) = self.__calculate_RGB(red, green, blue)

        # Send HTTP request
        intensityString = str(red_c) + "/" + str(green_c) + "/" + str(blue_c)
        response = self.__send_httprequest_out("triled", port, intensityString)
        return response

    def setBeak(self, redIntensity, greenIntensity, blueIntensity):
        """Set beak to a valid intensity. Each intensity should be an integer from 0 to 100."""

        response = self.__setTriLED(1, redIntensity, greenIntensity, blueIntensity)
        return response

    def setTail(self, port, redIntensity, greenIntensity, blueIntensity):
        """Set tail to a valid intensity. Port can be specified as 1, 2, 3, 4, or all.
        Each intensity should be an integer from 0 to 100."""

        # Triled port 1 is the beak. Tail starts counting at 2
        if not port == "all":
            port = port + 1

        response = self.__setTriLED(port, redIntensity, greenIntensity, blueIntensity)
        return response

    def __moveFinchAndWait(self, motion, direction, length, speed):
        """Send a command to move the finch and wait until the finch has finished
        its motion to return. Used by setMove and setTurn."""

        isMoving = self.__send_httprequest_in("finchIsMoving", "static")
        wasMoving = isMoving
        commandSendTime = time.time()
        done = False

        # Send HTTP request
        response = self.__send_httprequest_move(motion, direction, length, speed)

        while (not (done) and not (isMoving == "Not Connected")):
            wasMoving = isMoving
            time.sleep(0.01)
            isMoving = self.__send_httprequest_in("finchIsMoving", "static")
            done = ((time.time() > commandSendTime + 0.5) or (wasMoving == "true")) and (isMoving == "false")

        return response

    def setMove(self, direction, distance, speed):
        """Move the Finch forward or backward for a given distance at a given speed.
        Direction should be specified as 'F' or 'B'."""

        direction = self.__formatForwardBackward(direction)
        if direction is None:
            return 0

        distance = self.clampParametersToBounds(distance, -10000, 10000)
        speed = self.clampParametersToBounds(speed, 0, 100)

        response = self.__moveFinchAndWait("move", direction, distance, speed)

        return response

    def setTurn(self, direction, angle, speed):
        """Turn the Finch right or left to a given angle at a given speed.
        Direction should be specified as 'R' or 'L'."""

        direction = self.__formatRightLeft(direction)
        if direction is None:
            return 0

        angle = self.clampParametersToBounds(angle, -360000, 360000)
        speed = self.clampParametersToBounds(speed, 0, 100)

        response = self.__moveFinchAndWait("turn", direction, angle, speed)

        return response

    def setMotors(self, leftSpeed, rightSpeed):
        """Set the speed of each motor individually. Speed should be in
        the range of -100 to 100."""

        leftSpeed = self.clampParametersToBounds(leftSpeed, -100, 100)
        rightSpeed = self.clampParametersToBounds(rightSpeed, -100, 100)

        # Send HTTP request
        response = self.__send_httprequest_move("wheels", leftSpeed, rightSpeed, None)
        return response

    def stop(self):
        """Stop the Finch motors."""

        # Send HTTP request
        response = self.__send_httprequest_out("stopFinch", None, None)
        return response

    def resetEncoders(self):
        """Reset both encoder values to 0."""
        response = self.__send_httprequest_out("resetEncoders", None, None)

        # The finch needs a chance to actually reset
        time.sleep(0.2)

        return response

    # Finch Inputs
    def __getSensor(self, sensor, port):
        """Read the value of the specified sensor. Port should be specified as either 'R'
        or 'L'. If the port is not valid, returns -1."""

        # Early return if we can't execute the command because the port is invalid
        if ((not sensor == "finchOrientation") and (not port == "Left") and (not port == "Right") and
                (not ((port == "static") and (sensor == "Distance" or sensor == "finchCompass")))):
            return -1

        response = self.__send_httprequest_in(sensor, port)
        return response

    def getLight(self, direction):
        """Read the value of the right or left light sensor ('R' or 'L')."""

        direction = self.__formatRightLeft(direction)
        if direction is None:
            return 0

        response = self.__getSensor("Light", direction)
        return int(response)

    def getDistance(self):
        """Read the value of the distance sensor"""

        response = self.__getSensor("Distance", "static")
        return int(response)

    def getLine(self, direction):
        """Read the value of the right or left line sensor ('R' or 'L').
        Returns brightness as a value 0-100 where a larger number
        represents more reflected light."""

        direction = self.__formatRightLeft(direction)
        if direction is None:
            return 0

        response = self.__getSensor("Line", direction)
        return int(response)

    def getEncoder(self, direction):
        """Read the value of the right or left encoder ('R' or 'L').
        Values are returned in rotations."""

        direction = self.__formatRightLeft(direction)
        if direction is None:
            return 0

        response = self.__getSensor("Encoder", direction)
        encoder_value = round(float(response), 2)
        return encoder_value

    # The following methods override those within the Microbit
    # class to return values within the Finch reference frame.
    def getAcceleration(self):
        """Gives the acceleration of X,Y,Z in m/sec2, relative
        to the Finch's position."""

        return self._getXYZvalues("finchAccel", False)

    def getCompass(self):
        """Returns values 0-359 indicating the orentation of the Earth's
        magnetic field, relative to the Finch's position."""

        # Send HTTP request
        response = self.__getSensor("finchCompass", "static")
        compass_heading = int(response)
        return compass_heading

    def getMagnetometer(self):
        """Return the values of X,Y,Z of a magnetommeter, relative to the Finch's position."""

        return self._getXYZvalues("finchMag", True)

    def getOrientation(self):
        """Return the orentation of the Finch. Options include:
        "Beak up", "Beak down", "Tilt left", "Tilt right", "Level",
        "Upside down", and "In between"."""

        orientations = ["Beak%20Up", "Beak%20Down", "Tilt%20Left", "Tilt%20Right", "Level", "Upside%20Down"]
        orientation_result = ["Beak up", "Beak down", "Tilt left", "Tilt right", "Level", "Upside down"]

        # Check for orientation of each device and if true return that state
        for targetOrientation in orientations:
            response = self.__getSensor("finchOrientation", targetOrientation)
            if (response == "true"):
                return orientation_result[orientations.index(targetOrientation)]

        # If we are in a state in which none of the above seven states are true
        return "In between"

    # Finch Aliases
    acceleration = getAcceleration
    beak = setBeak
    compass = getCompass
    distance = getDistance
    encoder = getEncoder
    light = getLight
    line = getLine
    magnetometer = getMagnetometer
    motors = setMotors
    move = setMove
    orientation = getOrientation
    reset_encoders = resetEncoders
    tail = setTail
    turn = setTurn

    # END class Finch
