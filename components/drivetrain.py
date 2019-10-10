import wpilib
import wpilib.drive
import ctre
import navx

from modes import DrivetrainMode
from utils import *

class DrivetrainConstants:
    MAX_POWER = 0.5
    DEADZONE = 0.025

    K_TURNING = 0.04

class Drivetrain:
    differential_drivetrain: wpilib.drive.DifferentialDrive

    navx: navx.AHRS

    def __init__(self):
        self.drive_mode = DrivetrainMode.ASSIST_DRIVE_ARCADE

        self.x_power = 0
        self.z_rotation = 0
        self.l_power = 0
        self.r_power = 0

    def reset(self):
        self.differential_drivetrain.setDeadband(DrivetrainConstants.DEADZONE)
        self.differential_drivetrain.setMaxOutput(DrivetrainConstants.MAX_POWER)

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
        raw_rotation = rotation_error * DrivetrainConstants.K_TURNING
        self.z_rotation = math.copysign(abs(raw_rotation)**.5, raw_rotation)

    def arcade_drive(self, power, rotation):
        self.drive_mode = DrivetrainMode.MANUAL_DRIVE_ARCADE
        self.x_power = power
        self.z_rotation = rotation

    def curvature_drive(self, power, curvature):
        self.drive_mode = DrivetrainMode.MANUAL_DRIVE_CURVATURE
        self.x_power = power
        self.z_rotation = curvature

    def execute(self):
        if self.drive_mode == DrivetrainMode.ASSIST_DRIVE_ARCADE:
            self.differential_drivetrain.arcadeDrive(self.x_power, self.z_rotation)
        
        if self.drive_mode == DrivetrainMode.MANUAL_DRIVE_ARCADE:
            self.differential_drivetrain.arcadeDrive(self.x_power, self.z_rotation)
        
        if self.drive_mode == DrivetrainMode.MANUAL_DRIVE_CURVATURE:
            self.differential_drivetrain.curvatureDrive(self.x_power, self.z_rotation, True)

        if self.drive_mode == DrivetrainMode.MANUAL_DRIVE_TANK:
            self.differential_drivetrain.tankDrive(self.l_power, self.r_power)