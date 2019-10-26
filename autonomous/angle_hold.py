from components.drivetrain import *
from components.limelight import *
from wpilib import SmartDashboard as dash

import dashboard_utils
import robotmap

import os

class LimelightFollowAuto:
    MODE_NAME = "Angle Holding"
    DEFAULT = True

    subsystem_drivetrain: Drivetrain

    def on_enable(self):
        self.subsystem_drivetrain.reset()
        dash.putNumber("Turn Position", 0)
        self.subsystem_drivetrain.turn_to_angle(0)

    def on_disable(self):
        self.subsystem_drivetrain.stop_turning_to_angle()
        self.subsystem_drivetrain.reset()
        self.subsystem_drivetrain.arcade_drive(0, 0)

    def on_iteration(self, time_elapsed):
        dash.putBoolean("On Target", self.subsystem_drivetrain.is_done_turning())
        dash.putNumber("Distance from target", self.subsystem_drivetrain.turn_pid.getError())

        turn_kP, turn_kI, turn_kD = dashboard_utils.get_pid_values(robotmap.dashboard_pid_drivetrain_turn)
        self.subsystem_drivetrain.update_pid(turn_kP, turn_kI, turn_kD)

        self.subsystem_drivetrain.turn_to_angle(dash.getNumber("Turn Position", 0))