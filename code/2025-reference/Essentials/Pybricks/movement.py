from pybricks.hubs import EssentialHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase

hub = EssentialHub()

# Motors (example: A = left, B = right, one reversed)
left_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
right_motor = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)

# Adjust measurements for your robot
WHEEL_DIAMETER = 42.8  # mm
AXLE_TRACK = 78.4      # mm

robot = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)

def init_robot(default_speed: int = 500):
    """
    Initialize drive base with default speed (mm/s).
    Call once at program start.
    """
    robot.settings(straight_speed=default_speed)


def drive_cm(cm: float,
             velocity: int = 500,
             stop_mode=Stop.BRAKE):
    """
    Drive straight for 'cm' centimeters.
    +cm = forward, -cm = backward.
    Velocity in mm/s.
    """
    robot.settings(straight_speed=abs(velocity))  # set speed
    robot.straight(cm * 10)  # cm → mm

init_robot(default_speed=300)
drive_cm(-100)   # drive forward 100 cm
drive_cm(100)   # drive backward 50 cm