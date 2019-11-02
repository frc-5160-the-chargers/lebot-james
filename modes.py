import enum

class DrivetrainMode(enum.Enum):
    MANUAL_DRIVE_CURVATURE = enum.auto()
    
    MANUAL_DRIVE_TANK = enum.auto()

    MANUAL_DRIVE_ARCADE = enum.auto()

    ASSIST_DRIVE_ARCADE = enum.auto()

    TRAJECTORY_FOLLOW = enum.auto()

    TURN_TO_ANGLE = enum.auto()

    PROPORTIONAL_ANGLE_HOLDING = enum.auto()

class LoaderPosition(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()

class RobotModes(enum.Enum):
    MANUAL_DRIVE = enum.auto()

    AUTO_TARGETTING = enum.auto()