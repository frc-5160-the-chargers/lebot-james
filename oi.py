import wpilib

import utils

class OIConstants:
    CONTROLLER_DEADZONE = 0.1

    STRAIGHT_DEADZONE_HORIZONTAL = 0.15
    STRAIGHT_DEADZONE_VERTICAL = 0.1

class DriverStation:
    def __init__(self, driver_port=0, sysop_port=1):
        self.controller_driver = wpilib.XboxController(driver_port)
        self.controller_sysop = wpilib.XboxController(sysop_port)

    def curve_drivetrain(self, i):
        return utils.deadzone(i, OIConstants.CONTROLLER_DEADZONE) ** 3

    def check_drivetrain_straight(self, x, y):
        '''check and see if the input falls within the range needed to make the robot drive in a straight line'''
        return utils.deadzone(abs(x), OIConstants.STRAIGHT_DEADZONE_HORIZONTAL) == 0 and utils.deadzone(abs(y), OIConstants.STRAIGHT_DEADZONE_VERTICAL) != 0