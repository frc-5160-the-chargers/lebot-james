import magicbot
import wpilib
import wpilib.drive

import navx

from ctre import WPI_TalonSRX

import robotmap

from components import drivetrain
from oi import DriverStation

class LebotJames(magicbot.MagicRobot):
    subsystem_drivetrain: drivetrain.Drivetrain

    def createObjects(self):
        m_l_a = WPI_TalonSRX(robotmap.port_m_l_a)
        m_l_b = WPI_TalonSRX(robotmap.port_m_l_b)
        m_l_c = WPI_TalonSRX(robotmap.port_m_l_c)
        self.left_motors = wpilib.SpeedControllerGroup(m_l_a, m_l_b, m_l_c)

        m_r_a = WPI_TalonSRX(robotmap.port_m_r_a)
        m_r_b = WPI_TalonSRX(robotmap.port_m_r_b)
        m_r_c = WPI_TalonSRX(robotmap.port_m_r_c)
        self.right_motors = wpilib.SpeedControllerGroup(m_r_a, m_r_b, m_r_c)

        self.differential_drivetrain = wpilib.drive.DifferentialDrive(self.left_motors, self.right_motors)

        self.navx = navx.AHRS.create_spi()

        self.oi = DriverStation()

    def teleopInit(self):
        self.navx.reset()
        self.subsystem_drivetrain.reset()

    def teleopPeriodic(self):
        try:
            if self.subsystem_drivetrain.drive_mode == drivetrain.DrivetrainMode.MANUAL_DRIVE_CURVATURE:
                self.subsystem_drivetrain.curvature_drive(self.oi.controller_driver.getY()**3, -self.oi.controller_driver.getX()**3)
            if self.subsystem_drivetrain.drive_mode == drivetrain.DrivetrainMode.MANUAL_DRIVE_ARCADE:
                self.subsystem_drivetrain.arcade_drive(self.oi.controller_driver.getY()**3, -self.oi.controller_driver.getX()**3)
            
            if self.navx.isConnected() and self.oi.check_drivetrain_straight(self.oi.controller_driver.getX(), self.oi.controller_driver.getY()):
                self.subsystem_drivetrain.drive_to_angle(self.oi.controller_driver.getY()**3)
            elif self.subsystem_drivetrain.drive_mode == drivetrain.DrivetrainMode.ASSIST_DRIVE_ARCADE:
                self.subsystem_drivetrain.drive_mode = drivetrain.DrivetrainMode.MANUAL_DRIVE_CURVATURE
        except:
            self.onException()

def git_gud(robot):
    wpilib.run(robot)

if __name__ == '__main__':
    git_gud(LebotJames)