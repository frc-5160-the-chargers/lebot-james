from components.drivetrain import *
from components.limelight import *
import os

class LimelightFollowAuto:
    MODE_NAME = "Trajectory Following"
    DEFAULT = True

    subsystem_drivetrain: Drivetrain

    def on_enable(self):
        self.subsystem_drivetrain.reset()
        self.subsystem_drivetrain.set_trajectory("/home/lvuser/py/trajectories/test-trajectory.pickle")
        self.subsystem_drivetrain.drive_mode = DrivetrainMode.TRAJECTORY_FOLLOW

    def on_disable(self):
        self.subsystem_drivetrain.arcade_drive(0, 0)

    def on_iteration(self, time_elapsed):
        pass