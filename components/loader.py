from ctre import WPI_TalonSRX
from modes import LoaderPosition

class LoaderConstants:
    K_POWER_UP = 0.25
    K_POWER_DOWN = -0.25

class Loader:
    loader_motor: WPI_TalonSRX

    def __init__(self):
        self.reset()

    def reset(self):
        self.enabled = False
        self.position = LoaderPosition.UP

    def execute(self):
        if self.enabled:
            if self.position == LoaderPosition.UP:
                self.loader_motor.set(LoaderConstants.K_POWER_UP)
            elif self.position == LoaderPosition.DOWN:
                self.loader_motor.set(LoaderConstants.K_POWER_DOWN)
        else:
            self.loader_motor.set(0)