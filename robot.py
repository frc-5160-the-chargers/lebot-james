import magicbot
import wpilib
import wpilib.drive
from networktables import NetworkTables
from networktables import NetworkTablesInstance
from wpilib import SmartDashboard as dash

import navx

from ctre import WPI_TalonSRX

import robotmap
import dashboard_utils

from components import drivetrain, limelight
from oi import DriverStation

class LebotJames(magicbot.MagicRobot):
    subsystem_drivetrain: drivetrain.Drivetrain
    limelight: limelight.Limelight

    def createObjects(self):
        NetworkTables.initialize()

        m_l_a = WPI_TalonSRX(robotmap.port_m_l_a)
        m_l_b = WPI_TalonSRX(robotmap.port_m_l_b)
        m_l_c = WPI_TalonSRX(robotmap.port_m_l_c)
        self.left_motors = wpilib.SpeedControllerGroup(m_l_a, m_l_b, m_l_c)
        self.encoder_controller_left = m_l_a

        m_r_a = WPI_TalonSRX(robotmap.port_m_r_a)
        m_r_b = WPI_TalonSRX(robotmap.port_m_r_b)
        m_r_c = WPI_TalonSRX(robotmap.port_m_r_c)
        self.right_motors = wpilib.SpeedControllerGroup(m_r_a, m_r_b, m_r_c)
        self.encoder_controller_right = m_r_a

        self.differential_drivetrain = wpilib.drive.DifferentialDrive(self.left_motors, self.right_motors)

        self.navx = navx.AHRS.create_spi()

        self.oi = DriverStation()

        dashboard_utils.put_pid_values(
            "drivetrain_turn",
            kP=drivetrain.DrivetrainConstants.K_TURN_P,
            kI=drivetrain.DrivetrainConstants.K_TURN_I, 
            kD=drivetrain.DrivetrainConstants.K_TURN_D
        )

    def teleopInit(self):
        self.navx.reset()
        self.subsystem_drivetrain.reset()
        self.limelight.reset()

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

            dash.putString("distance to target", self.limelight.get_distance_trig(31, 51))
            dash.putString("horizontal angle to target", self.limelight.get_horizontal_angle_offset())
            dash.putString("vertical angle to target", self.limelight.get_vertical_angle_offset())
        except:
            self.onException()

def git_gud(robot):
    wpilib.run(robot)

if __name__ == '__main__':
    git_gud(LebotJames)