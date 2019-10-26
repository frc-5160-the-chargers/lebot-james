from wpilib import SmartDashboard as dash

def get_pid_values(controller_name):
    kP = dash.getNumber(f"{controller_name}_kP", 0)
    kI = dash.getNumber(f"{controller_name}_kI", 0)
    kD = dash.getNumber(f"{controller_name}_kD", 0)

    return kP, kI, kD

def put_pid_values(controller_name, kP=0, kI=0, kD=0):
    dash.putNumber(f"{controller_name}_kP", kP)
    dash.putNumber(f"{controller_name}_kI", kI)
    dash.putNumber(f"{controller_name}_kD", kD)