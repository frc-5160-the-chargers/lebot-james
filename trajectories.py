import pathfinder as pf

import json
import pickle

def load_trajectories_json(trajectory_name, filename='trajectories.json'):
    with open(filename, 'r') as f:
        json_data = json.load(f)
        trajectory_points = json_data[trajectory_name]

    points = [pf.Waypoint(i[0], i[1], i[2]) for i in trajectory_points]
    return points

def generate_trajectory(points, max_velocity, max_acceleration, max_jerk, time_step=.05):
    info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
                                    dt=time_step,
                                    max_velocity=max_velocity,
                                    max_acceleration=max_acceleration,
                                    max_jerk=max_jerk)
    return trajectory

def modify_trajectory_tank(trajectory, drivetrain_width):
    modifier = pf.modifiers.TankModifier(trajectory).modify(drivetrain_width)
    return modifier

def save_trajectory(trajectory, filename):
    with open(filename, 'wb') as f:
        pickle.dump(trajectory, f)
    
def load_trajectory(filename):
    with open(filename, 'rb') as f:
        trajectory = pickle.load(f)
    return trajectory

def get_tank_trajectory_data(modifier):
    return pf.followers.EncoderFollower(modifier.getLeftTrajectory()), pf.followers.EncoderFollower(modifier.getRightTrajectory())

if __name__ == '__main__':
    generate = False
    json_filename = 'trajectories.json'
    with open(json_filename, 'r') as f:
        json_data = json.load(f)

    trajectories = []

    for trajectory_name in json_data:
        if generate:
            points = load_trajectories_json(trajectory_name, json_filename)
            trajectory = generate_trajectory(points, 0.5, 0.1, 0.5)
            trajectory = modify_trajectory_tank(trajectory, 22/12)
            save_trajectory(trajectory, f'./{trajectory_name}.pickle')
            trajectories.append(trajectory)
        else:
            trajectory = load_trajectory(f'./{trajectory_name}.pickle')
            trajectories.append(trajectory)

    for trajectory in trajectories:
        print(get_tank_trajectory_data(trajectory))