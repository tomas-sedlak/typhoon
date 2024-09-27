import math
from typhoon.utils import config

def angles_from_coords(x: int, y: int, z: int) -> tuple[float, float, float]:
    """
    Calculates joint angles from Cartesian coordinates.

    Args:
        x: The x-coordinate.
        y: The y-coordinate.
        z: The z-coordinate.

    Returns:
        A tuple of joint angles (q1, q2, q3).
    """

    r = math.sqrt(x**2 + y**2)
    q1 = math.atan2(y, x)
    q3 = math.acos((r**2 + z**2 - config.LENGTH_LOWER_ARM**2 - config.LENGTH_UPPER_ARM**2) / (2 * config.LENGTH_LOWER_ARM * config.LENGTH_UPPER_ARM))
    q2 = math.atan2(z, r) + math.atan2(config.LENGTH_UPPER_ARM * math.sin(q3), config.LENGTH_LOWER_ARM + config.LENGTH_UPPER_ARM * math.cos(q3))

    return q1, q2, q3

def steps_from_angle(angle: float) -> int:
    """
    Calculates the number of steps required to rotate to a given angle.

    Args:
        angle: The target angle in radians.

    Returns:
        The number of steps required.
    """
    return int((angle * config.STEPS_PER_REVOLUTION) / (2 * math.pi))