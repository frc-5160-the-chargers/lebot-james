import networktables

from networktables import NetworkTables

class Limelight:    
    def __init__(self):
        self.reset()
        self.limelight_table = NetworkTables.getTable("limelight")

    def get_angle_offset(self):
        '''return the angle needed to turn to make the target in the center of view'''
        if self.valid_target:
            return self.horizontal_offset
        else:
            return 0

    def reset(self):
        self.valid_target = False
        self.horizontal_offset = 0
        self.vertical_offset = 0
        self.target_area = 0

    def execute(self):
        targets = self.limelight_table.getNumber('tv', None)
        self.valid_target = targets >= 1.0 if targets != None else False
        print(targets)

        if self.valid_target:
            print("asdf")
            self.horizontal_offset = self.limelight_table.getNumber('tx', None)
            self.vertical_offset = self.limelight_table.getNumber('ty', None)
            self.target_area = self.limelight_table.getNumber('ta', None)