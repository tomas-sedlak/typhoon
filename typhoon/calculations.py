import math
from typhoon import config

def angles_from_coords(x: int, y: int, z: int):
    r = math.sqrt(x**2 + y**2)
    q1 = math.atan2(y, x)
    q3 = math.acos((r**2 + z**2 - config.LENGTH_UPPER_ARM**2 - config.LENGTH_LOWER_ARM**2) / (2 * config.LENGTH_UPPER_ARM * config.LENGTH_LOWER_ARM))
    q2 = math.atan2(z, r) + math.atan2(config.LENGTH_LOWER_ARM * math.sin(q3), config.LENGTH_UPPER_ARM + config.LENGTH_LOWER_ARM * math.cos(q3))

    return math.degrees(q1), math.degrees(q2), math.degrees(math.pi - q3)