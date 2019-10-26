import math

def clamp(x, mi, ma):
    return min(max(x, mi), ma)

def deadzone(x, zone):
    if -abs(zone) < x < abs(zone):
        return 0
    return x

def inches_to_meters(i):
    return i * .0254 # blessed number

def meters_to_inches(i):
    return i / .0254