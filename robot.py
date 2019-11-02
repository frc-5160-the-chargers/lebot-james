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

from components import drivetrain, limelight, shooter, loader
from modes import *
from oi import DriverStation

class LebotJames(magicbot.MagicRobot):
    if robotmap.drivetrain_enabled:
        subsystem_drivetrain: drivetrain.Drivetrain

    if robotmap.shooter_enabled:
        subsystem_shooter: shooter.Shooter

    if robotmap.loader_enabled:
        subsystem_loader: loader.Loader

    if robotmap.limelight_enabled:
        limelight: limelight.Limelight

    def createObjects(self):
        NetworkTables.initialize()

        if robotmap.drivetrain_enabled:
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

        if robotmap.shooter_enabled:
            self.shooter_motor = WPI_TalonSRX(robotmap.port_m_shooter)

        if robotmap.loader_enabled:
            self.loader_motor = WPI_TalonSRX(robotmap.port_m_loader)

        if robotmap.navx_enabled:
            self.navx = navx.AHRS.create_spi()

        self.oi = DriverStation()

        dashboard_utils.put_pid_values(
            robotmap.dashboard_pid_drivetrain_turn,
            kP=drivetrain.DrivetrainConstants.K_TURN_P,
            kI=drivetrain.DrivetrainConstants.K_TURN_I, 
            kD=drivetrain.DrivetrainConstants.K_TURN_D
        )

        self.robot_mode = RobotModes.MANUAL_DRIVE

    def reset_subsystems(self):
        if robotmap.navx_enabled:
            self.navx.reset()
        if robotmap.drivetrain_enabled:
            self.subsystem_drivetrain.reset()
        if robotmap.shooter_enabled:
            self.subsystem_shooter.reset()
        if robotmap.limelight_enabled:
            self.limelight.reset()
        self.robot_mode = RobotModes.MANUAL_DRIVE

    def teleopInit(self):
        self.reset_subsystems()

    def teleopPeriodic(self):
        try:
            if self.robot_mode == RobotModes.MANUAL_DRIVE:
                if robotmap.drivetrain_enabled:
                    if self.subsystem_drivetrain.drive_mode == drivetrain.DrivetrainMode.MANUAL_DRIVE_CURVATURE:
                        self.subsystem_drivetrain.curvature_drive(self.oi.controller_driver.getY()**3, -self.oi.controller_driver.getX()**3)
                    if self.subsystem_drivetrain.drive_mode == drivetrain.DrivetrainMode.MANUAL_DRIVE_ARCADE:
                        self.subsystem_drivetrain.arcade_drive(self.oi.controller_driver.getY()**3, -self.oi.controller_driver.getX()**3)
                    
                    if self.navx.isConnected() and self.oi.check_drivetrain_straight(self.oi.controller_driver.getX(), self.oi.controller_driver.getY()):
                        self.subsystem_drivetrain.drive_to_angle(self.oi.controller_driver.getY()**3)
                    elif self.subsystem_drivetrain.drive_mode == drivetrain.DrivetrainMode.ASSIST_DRIVE_ARCADE:
                        self.subsystem_drivetrain.drive_mode = drivetrain.DrivetrainMode.MANUAL_DRIVE_CURVATURE

                if robotmap.shooter_enabled:
                    target_shooter_speed = dash.getNumber("target shooter velocity", 0)
                    shooter_enabled = dash.getBoolean("shooter enabled", False)

                    if shooter_enabled:
                        self.subsystem_shooter.enable_at_speed(self.oi.controller_driver.getY(wpilib.XboxController.Hand.kLeft))
                    else:
                        self.subsystem_shooter.disable()

                    dash.putNumber("shooter speed error", self.subsystem_shooter.get_error())
            
                if robotmap.loader_enabled:
                    if self.oi.controller_driver.getPOV() == 0: # up on dpad
                        self.subsystem_loader.position = LoaderPosition.UP
                    if self.oi.controller_driver.getPOV() == 180: # down on dpad
                        self.subsystem_loader.position = LoaderPosition.DOWN
                    if self.oi.controller_driver.getXButtonPressed():
                        self.subsystem_loader.enabled = not self.subsystem_loader.enabled

                if self.oi.controller_driver.getBButtonPressed():
                    self.robot_mode = RobotModes.AUTO_TARGETTING
            
            elif self.robot_mode == RobotModes.AUTO_TARGETTING:
                # this is the control loop that will deal with automatically shooting into a target
                # inputs: distance from target, horizontal offset from target
                # outputs: speed of shooter, turning speed of robot, linear speed of robot
                # the speed of the shooter is controlled by the distance
                # the linear speed of the robot is controlled by the distance
                # the turning speed of the robot is controlled by the horizontal offset of the robot

                if not robotmap.limelight_enabled:
                    # we can't do anything in this case.
                    self.robot_mode = RobotModes.MANUAL_DRIVE

                distance_to_target = self.limelight.get_distance_trig()
                x_offset = self.limelight.get_horizontal_angle_offset()

                drivetrain_on_target = True

                if robotmap.drivetrain_enabled:
                    # use proportional techniques to make the robot drive into a good position to shoot
                    angular_error = 0
                    distance_error = 0

                    if abs(x_offset) > robotmap.auto_targetting_alignment_tolerance:
                        drivetrain_on_target = False
                        angular_error = 0-x_offset
                    
                    if distance_to_target > robotmap.auto_targetting_max_distance:
                        drivetrain_on_target = False
                        distance_error = distance_to_target - robotmap.auto_targetting_max_distance
                    
                    if distance_to_target < robotmap.auto_targetting_min_distance:
                        drivetrain_on_target = False
                        distance_to_target = distance_to_target - robotmap.auto_targetting_min_distance

                    drivetrain_rotation = drivetrain.DrivetrainConstants.K_PROPORTIONAL_TURNING*angular_error
                    drivetrain_power = drivetrain.DrivetrainConstants.K_PROPORTIONAL_DRIVING*distance_error

                    self.subsystem_drivetrain.arcade_drive(-drivetrain_power, drivetrain_rotation)

                if robotmap.shooter_enabled:
                    # set the shooter to an appropriate speed if the drivetrain is on target
                    if drivetrain_on_target:
                        self.subsystem_shooter.enabled = True
                        self.subsystem_shooter.shoot_from_distance(distance_to_target, angle=45)
                    else:
                        self.subsystem_shooter.enabled = False

                if robotmap.loader_enabled:
                    # TODO: we don't have a working loader right now so (logically) there's no code here
                    pass

                if self.oi.controller_driver.getBButtonPressed():
                    self.robot_mode = RobotModes.MANUAL_DRIVE

            if robotmap.limelight_enabled:
                dash.putString("distance to target", self.limelight.get_distance_trig())
                dash.putString("horizontal angle to target", self.limelight.get_horizontal_angle_offset())
                dash.putString("vertical angle to target", self.limelight.get_vertical_angle_offset())

        except:
            self.onException()

if __name__ == '__main__':
    wpilib.run(LebotJames)