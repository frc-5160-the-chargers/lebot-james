from components.drivetrain import *
from components.limelight import *
import os

class LimelightFollowAuto:
    MODE_NAME = "Angle Holding"
    DEFAULT = True

    subsystem_drivetrain: Drivetrain

    def on_enable(self):
        self.subsystem_drivetrain.reset()
        self.subsystem_drivetrain.turn_to_angle(0)

    def on_disable(self):
        self.subsystem_drivetrain.reset()
        self.subsystem_drivetrain.arcade_drive(0, 0)

    def on_iteration(self, time_elapsed):
        pass