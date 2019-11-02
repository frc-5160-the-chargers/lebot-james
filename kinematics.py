import math

def calculate_shot_vector(starting_position=(0, 0), target_position=(0, 0), shooting_angle=-1, target_angle=-1):
    '''
    calculate the launch vector required for a basic ballistic trajectory
    params:
        starting_position: vector of initial position (for offsets and such)
        target_position: position of the target relative to (0, 0)
        shooting_angle: angle constraint for making the shot -- if -1 then doesn't use as constraint
        target_angle: angle at which to land in the target -- if -1 then doesn't use as constraint
    returns:
        ((launch vector), shooting_angle, target_angle, time_of_intercept, valid_launch)
    '''
    # much of the math behind this kinematic nonsense can be found here
    
    shooting_angle_constrained = shooting_angle != -1
    target_angle_constrained = target_angle != -1

    if shooting_angle_constrained == target_angle_constrained:
        # we can't have both or neither be constrained
        return ((0, 0), shooting_angle, target_angle, -1, False)

    displacement = (target_position[0]-starting_position[0], target_position[1]-starting_position[1])
    X = displacement[0]
    Y = displacement[1]
    g = 9.8

    v_x = 0
    v_y = 0

    time_of_intercept = 0


    rad_angle = math.radians(shooting_angle)

    if target_angle_constrained:
        # https://www.desmos.com/calculator/ozhed2yvau
        v_x = math.sqrt((g * X**2) / (2 * (X * math.tan(rad_angle) + Y)))
        v_y = -(((-g * X) / v_x) + (v_x * math.tan(rad_angle)))

    if shooting_angle_constrained:
        # ensure that we can hit the target given the constraint -- if v_y is below a certain line then it's impossible
        # TODO THIS NONSENSE ONLY WORKS WITH 45* AND I HATE THAT
        # https://www.desmos.com/calculator/4mxmqmsycg
        if Y < math.tan(rad_angle) * X:
            return ((0, 0), shooting_angle, target_angle, -1, False)

        v_y = math.sqrt(((X ** 2) * g * math.tan(rad_angle) ** 2) / ((-2 * Y) + (2 * X * math.tan(rad_angle))))
        v_x = v_y / math.tan(rad_angle)

    time_of_intercept = X / v_x
    target_angle = math.degrees(math.atan2(-g * time_of_intercept + v_y, v_x))
    shooting_angle = math.degrees(math.atan2(v_y, v_x))
    return ((v_x, v_y), shooting_angle, target_angle, time_of_intercept, True)