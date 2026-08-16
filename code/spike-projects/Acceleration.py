"""Python port of the 'Acceleration' My Block (Acceleration.llsp3), for testing
on the hub via the SPIKE App's Python canvas. The Word Blocks version is the
team's default per code/README.md — this is being tried alongside it, not
replacing it, until it's confirmed to drive the same as the block version.

drive_ramp ramps from start_speed to end_speed over the first `acceleration`
degrees of motor rotation, cruises at end_speed, then ramps back down to
start_speed over the last `acceleration` degrees before `degrees` is reached.
The gyro continuously trims left/right speed to keep it driving straight.
"""
from spike import PrimeHub, Motor, MotorPair
from spike.control import wait_for_seconds

hub = PrimeHub()
motors = MotorPair('A', 'B')
reference_motor = Motor('B')


def drive_ramp(end_speed, start_speed, degrees, acceleration):
    reference_motor.set_degrees_counted(0)
    wait_for_seconds(0.3)
    hub.motion_sensor.reset_yaw_angle()

    gyro_error = 0
    gyro_last_error = 0

    # Phase 1: ramp up from start_speed to end_speed over the first
    # `acceleration` degrees.
    while reference_motor.get_degrees_counted() < acceleration:
        gyro_error = hub.motion_sensor.get_yaw_angle()
        gyro_correction = (gyro_error * 2) + (gyro_last_error - gyro_error)
        base_speed = (end_speed - start_speed) * (
            reference_motor.get_degrees_counted() / acceleration
        ) + start_speed
        motors.start_tank(base_speed - gyro_correction, base_speed + gyro_correction)
        gyro_last_error = gyro_error

    # Phase 2: cruise at end_speed until `acceleration` degrees remain.
    while reference_motor.get_degrees_counted() <= (degrees - acceleration):
        gyro_error = hub.motion_sensor.get_yaw_angle()
        gyro_correction = (gyro_error * -2) + (gyro_last_error - gyro_error)
        motors.start_tank(end_speed + gyro_correction, end_speed - gyro_correction)
        gyro_last_error = gyro_error

    # Phase 3: ramp down from end_speed to start_speed over the last
    # `acceleration` degrees.
    while reference_motor.get_degrees_counted() < degrees:
        gyro_error = hub.motion_sensor.get_yaw_angle()
        gyro_correction = (gyro_error * -2) + (gyro_last_error - gyro_error)
        base_speed = (start_speed - end_speed) * (
            (reference_motor.get_degrees_counted() - degrees) / acceleration
        ) + start_speed
        motors.start_tank(base_speed + gyro_correction, base_speed - gyro_correction)
        gyro_last_error = gyro_error

    motors.stop()


drive_ramp(end_speed=50, start_speed=20, degrees=1000, acceleration=400)
