import wpilib
from ctre import WPI_TalonSRX

import math

import utils

import kinematics

class ShooterConstants:
    PID_ENABLED = False

    K_P = 0
    K_I = 0
    K_D = 0

    SHOOTER_DIAMETER = 4

    # TODO ensure that these are correct
    SHOOTER_HEIGHT = 30
    TARGET_HEIGHT = 30

    K_RAD_S_POWER = 0.2 # radians per second per 100% power

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

    def shoot_from_distance(self, distance, angle=45):
        '''set the shooter speed to be the correct one given a distance and firing angle'''
        # TODO make sure everything is in meters because SI good imperial bad
        vector, _, _, time_intercept, valid = kinematics.calculate_shot_vector(starting_position=(0, ShooterConstants.SHOOTER_HEIGHT), target_position=(distance, ShooterConstants.TARGET_HEIGHT), shooting_angle=angle)
        if not valid:
            self.set_motors(0)
            return -1
        tangential_speed = math.hypot(vector[0], vector[1])
        angular_speed = tangential_speed / (ShooterConstants.SHOOTER_DIAMETER / 2)
        rotation_power = angular_speed * ShooterConstants.K_RAD_S_POWER
        self.set_motors(rotation_power)
        return rotation_power

    def execute(self):
        if not self.enabled:
            self.set_motors(0)