import math

def clamp(x, mi, ma):
    return min(max(x, mi), ma)

def deadzone(x, zone):
    if -abs(zone) < x < abs(zone):
        return 0
    return x