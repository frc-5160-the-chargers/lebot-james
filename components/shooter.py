import wpilib
from ctre import WPI_TalonSRX

import math

import utils

class ShooterConstants:
    PID_ENABLED = False

    K_P = 0
    K_I = 0
    K_D = 0

    SHOOTER_DIAMETER = 4

class Shooter:
    shooter_motor: WPI_TalonSRX

    def __init__(self):
        if ShooterConstants.PID_ENABLED:
            self.speed_controller_pid = wpilib.PIDController(
                ShooterConstants.K_P,
                ShooterConstants.K_I,
                ShooterConstants.K_D,
                lambda: self.get_linear_velocity(),
                lambda x: self.set_motors(x)
            )
            self.speed_controller_pid.setOutputRange(-1, 1)

        self.enabled = False

    def reset(self):
        if ShooterConstants.PID_ENABLED:
            self.speed_controller_pid.disable()
            self.shooter_motor.setEncPosition(0)
        self.set_motors(0)

    def get_rotational_velocity(self):
        '''get the rotational velocity in rotations per minute'''
        # TODO update this to use the actual motor controller
        # return self.shooter_motor.getEncoder().getVelocity()
        return 0

    def get_linear_velocity(self):
        '''get the linear velocity in meters per second'''
        # TODO update this to use the actual motor controller
        # rotations_per_minute = self.get_rotational_velocity()
        # rotations_per_second = rotations_per_minute / 60
        # rad_per_second = rotations_per_second * 2 * math.pi
        # return rad_per_second * utils.inches_to_meters(ShooterConstants.SHOOTER_DIAMETER) / 2
        return 0

    def set_motors(self, power):
        self.shooter_motor.set(power)

    def set_speed(self, speed):
        if ShooterConstants.PID_ENABLED:
            self.speed_controller_pid.setSetpoint(speed)

    def enable_at_speed(self, speed=0):
        if ShooterConstants.PID_ENABLED:
            self.speed_controller_pid.enable()
            self.set_speed(speed)
        self.enabled = True
    
    def disable(self):
        if ShooterConstants.PID_ENABLED:
            self.speed_controller_pid.disable()
        self.enabled = False

    def get_error(self):
        if ShooterConstants.PID_ENABLED:
            return self.speed_controller_pid.getError()
        else:
            return 0

    def execute(self):
        if not self.enabled:
            self.set_motors(0)