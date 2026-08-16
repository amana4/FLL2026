from pybricks.hubs import EssentialHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase

hub = EssentialHub()

# One motor runs clockwise, the other counterclockwise
left_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)

# Adjust measurements for your robot
wheel_diameter = 42.8  # mm
axle_track = 78.4      # mm

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

# Move forward 10 cm (100 mm)
robot.straight(-1000)
robot.straight(1000)


robot.stop(Stop.BRAKE)