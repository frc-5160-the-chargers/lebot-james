from components.drivetrain import *
from components.limelight import *

class LimelightFollowAuto:
    MODE_NAME = "Limelight Following"
    DEFAULT = True

    subsystem_drivetrain: Drivetrain
    limelight: Limelight

    def on_enable(self):
        self.subsystem_drivetrain.reset()
        self.limelight.reset()

    def on_disable(self):
        self.subsystem_drivetrain.arcade_drive(0, 0)

    def on_iteration(self, time_elapsed):
        limelight_displacement = self.limelight.get_horizontal_angle_offset()
        self.subsystem_drivetrain.arcade_drive(0, -limelight_displacement*DrivetrainConstants.K_TURNING)