import enum

class DrivetrainMode(enum.Enum):
    MANUAL_DRIVE_CURVATURE = enum.auto()
    
    MANUAL_DRIVE_TANK = enum.auto()

    MANUAL_DRIVE_ARCADE = enum.auto()

    ASSIST_DRIVE_ARCADE = enum.auto()