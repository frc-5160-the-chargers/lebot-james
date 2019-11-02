import wpilib
import wpilib.drive
import ctre
import navx

from modes import DrivetrainMode
from utils import *

class DrivetrainConstants:
    MAX_POWER = 0.5
    DEADZONE = 0.025

    K_PROPORTIONAL_TURNING = 0.04
    K_PROPORTIONAL_DRIVING = 0.05

    WHEEL_DIAMETER = 6

    K_TURN_P = 0
    K_TURN_I = 0
    K_TURN_D = 0

class Drivetrain:
    differential_drivetrain: wpilib.drive.DifferentialDrive
    encoder_controller_left: ctre.WPI_TalonSRX
    encoder_controller_right: ctre.WPI_TalonSRX

    navx: navx.AHRS

    def __init__(self):
        self.drive_mode = DrivetrainMode.ASSIST_DRIVE_ARCADE

        self.x_power = 0
        self.z_rotation = 0
        self.l_power = 0
        self.r_power = 0

        self.turn_pid = wpilib.PIDController(
            DrivetrainConstants.K_TURN_P,
            DrivetrainConstants.K_TURN_I,
            DrivetrainConstants.K_TURN_D,
            lambda: self.navx.getAngle(),
            lambda x: self.differential_drivetrain.arcadeDrive(0, x)
        )
        self.turn_pid.setOutputRange(-1, 1)

    def reset(self):
        self.differential_drivetrain.setDeadband(DrivetrainConstants.DEADZONE)
        self.differential_drivetrain.setMaxOutput(DrivetrainConstants.MAX_POWER)
        self.turn_pid.disable()

    def reset_encoders(self):
        self.encoder_controller_left.setQuadraturePosition(0)
        self.encoder_controller_right.setQuadraturePosition(0)

    def get_positions(self):
        '''return the position of the left and right side'''
        return self.encoder_controller_left.getQuadraturePosition(), self.encoder_controller_right.getQuadraturePosition()

    def get_velocities(self):
        '''return the velocity of the left and right side'''
        return self.encoder_controller_left.getQuadratureVelocity(), self.encoder_controller_right.getQuadratureVelocity()

    def get_average_position(self):
        l_p, r_p = self.get_positions()
        return (l_p+r_p)/2

    def get_average_velocity(self):
        l_v, r_v = self.get_velocities()
        return (l_v+r_v)/2

    def update_pid(self, kP=0, kI=0, kD=0):
        self.turn_pid.setPID(kP, kI, kD)
        
    def tank_drive(self, left_power, right_power):
        self.drive_mode = DrivetrainMode.MANUAL_DRIVE_TANK
        self.l_power = left_power
        self.r_power = right_power

    def drive_to_angle(self, power, angle=0):
        if self.drive_mode != DrivetrainMode.ASSIST_DRIVE_ARCADE:
            self.drive_mode = DrivetrainMode.ASSIST_DRIVE_ARCADE
            self.navx.reset()
        self.x_power = power

        rotation_error = self.navx.getAngle() - angle
        raw_rotation = rotation_error * DrivetrainConstants.K_PROPORTIONAL_TURNING
        self.z_rotation = math.copysign(abs(raw_rotation)**.5, raw_rotation)

    def arcade_drive(self, power, rotation):
        self.drive_mode = DrivetrainMode.MANUAL_DRIVE_ARCADE
        self.x_power = power
        self.z_rotation = rotation

    def curvature_drive(self, power, curvature):
        self.drive_mode = DrivetrainMode.MANUAL_DRIVE_CURVATURE
        self.x_power = power
        self.z_rotation = curvature

    def turn_to_angle(self, angle, tolerance=1):
        if self.drive_mode != DrivetrainMode.TURN_TO_ANGLE:
            self.turn_pid.setAbsoluteTolerance(tolerance)
            self.drive_mode = DrivetrainMode.TURN_TO_ANGLE
            self.turn_pid.reset()
            self.turn_pid.enable()
        self.turn_pid.setSetpoint(angle)

    def stop_turning_to_angle(self):
        self.turn_pid.disable()
        self.drive_mode = DrivetrainMode.MANUAL_DRIVE_CURVATURE

    def is_done_turning(self):
        if self.drive_mode != DrivetrainMode.TURN_TO_ANGLE:
            return False
        return self.turn_pid.onTarget()
 
    def execute(self):
        if self.drive_mode == DrivetrainMode.ASSIST_DRIVE_ARCADE:
            self.differential_drivetrain.arcadeDrive(self.x_power, self.z_rotation)
        
        if self.drive_mode == DrivetrainMode.MANUAL_DRIVE_ARCADE:
            self.differential_drivetrain.arcadeDrive(self.x_power, self.z_rotation)
        
        if self.drive_mode == DrivetrainMode.MANUAL_DRIVE_CURVATURE:
            self.differential_drivetrain.curvatureDrive(self.x_power, self.z_rotation, True)

        if self.drive_mode == DrivetrainMode.MANUAL_DRIVE_TANK:
            self.differential_drivetrain.tankDrive(self.l_power, self.r_power)

        if self.drive_mode == DrivetrainMode.TURN_TO_ANGLE:
            pass