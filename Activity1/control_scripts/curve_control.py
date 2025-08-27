#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from autoware_auto_control_msgs.msg import AckermannControlCommand, AckermannLateralCommand, LongitudinalCommand
from nav_msgs.msg import Odometry
import math

class VehicleController(Node):
    def __init__(self, target_yaw=math.pi/2, pre_delay=2.0, post_delay=2.0, curve_gain = 1.0, velocity_change=0.0):
        super().__init__('vehicle_controller')

        self.publisher_ = self.create_publisher(AckermannControlCommand,
                                                '/simulation/actuation/control_command', 10)
        self.subscription = self.create_subscription(Odometry,
                                                     '/simulation/sensor/odometry',
                                                     self.odometry_callback, 10)

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.current_speed = 0.0
        self.current_position = (0.0, 0.0, 0.0)
        self.current_yaw = 0.0

        self.target_yaw = target_yaw
        self.pre_delay = pre_delay
        self.post_delay = post_delay
        self.velocity_change = velocity_change
        self.curve_gain = curve_gain

        self.start_time = self.get_clock().now().nanoseconds / 1e9
        self.curve_started = False
        self.curve_finished = False
        self.post_start_time = 0.0

        self.max_speed = 10.0
        self.base_acceleration = 1.0

        self.get_logger().info("Vehicle control node started.")

    def odometry_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        self.current_position = (x, y, z)

        q = msg.pose.pose.orientation
        yaw = quaternion_to_yaw(q.x, q.y, q.z, q.w)
        self.current_yaw = yaw

        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        self.current_speed = math.sqrt(vx**2 + vy**2)

    def timer_callback(self):
        t = self.get_clock().now().nanoseconds / 1e9 - self.start_time
        msg = AckermannControlCommand()
        msg.stamp = self.get_clock().now().to_msg()

        longitudinal = LongitudinalCommand()
        if not self.curve_started:
            if t < self.pre_delay:
                longitudinal.acceleration = self.base_acceleration
            else:
                self.curve_started = True
                self.get_logger().info("Starting curve")
        elif self.curve_started and not self.curve_finished:
            longitudinal.acceleration = self.base_acceleration + self.velocity_change
        elif self.curve_finished:
            if t - self.post_start_time < self.post_delay:
                longitudinal.acceleration = -self.base_acceleration
            else:
                longitudinal.acceleration = 0.0
                self.get_logger().info("Finished maneuver")
                self.destroy_node()
                rclpy.shutdown()
                return

        longitudinal.speed = 0.0
        longitudinal.jerk = 0.0

        lateral = AckermannLateralCommand()
        if self.curve_started and not self.curve_finished:
            yaw_error = self.target_yaw - self.current_yaw

            if abs(yaw_error) > 0.01:
                lateral.steering_tire_angle = yaw_error * self.curve_gain
            else:
                lateral.steering_tire_angle = 0.0
                self.curve_finished = True
                self.post_start_time = t
                self.get_logger().info("Reached target rotation")
        else:
            lateral.steering_tire_angle = 0.0

        lateral.steering_tire_rotation_rate = 0.0

        msg.longitudinal = longitudinal
        msg.lateral = lateral
        self.publisher_.publish(msg)

        x, y, _ = self.current_position
        self.get_logger().info(f"t={t:.2f}s, pos -> x:{x:.2f}, y:{y:.2f}, speed:{self.current_speed:.2f} m/s, yaw={self.current_yaw:.2f} rad, steering angle {lateral.steering_tire_angle:.2f} rad")
    
def quaternion_to_yaw(qx, qy, qz, qw):
    siny_cosp = 2.0 * (qw * qz + qx * qy)
    cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    return yaw

def main(args=None):
    import sys
    rclpy.init(args=args)

    # Define parameter sets
    parameter_sets = {
        "straight": {
            "target_yaw": 0.0,
            "pre_delay": 2.0,
            "post_delay": 2.0,
            "curve_gain": 0.0,
            "velocity_change": 0.0
        },
        "gentle": {
            "target_yaw": math.pi/6,  # 30 degrees
            "pre_delay": 2.0,
            "post_delay": 2.0,
            "curve_gain": 3.0,
            "velocity_change": 0.0
        },
        "medium": {
            "target_yaw": math.pi/2,  # 90 degrees
            "pre_delay": 2.0,
            "post_delay": 2.0,
            "curve_gain": 6.0,
            "velocity_change": 0.0
        },
        "tight": {
            "target_yaw": math.pi,  # 180 degrees
            "pre_delay": 2.0,
            "post_delay": 2.0,
            "curve_gain": 10.0,
            "velocity_change": 0.0
        }
    }

    if len(sys.argv) > 1:
        selection = sys.argv[1].lower()
        if selection not in parameter_sets:
            print(f"Unknown selection '{selection}'. Valid options: {list(parameter_sets.keys())}")
            return
    else:
        print("No selection provided. Defaulting to 'tight'.")
        selection = "tight"

    params = parameter_sets[selection]
    print(f"Running with parameter set: {selection}")
    node = VehicleController(**params)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
