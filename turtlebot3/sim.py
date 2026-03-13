import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped, TransformStamped
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster

WHEEL_RADIUS = 0.033
FREQUENCY_HZ = 50
SPEED = 0.05


class TurtleBot3Sim(Node):
    def __init__(self):
        super().__init__("turtlebot3_sim")

        self.declare_parameter("frequency_hz", FREQUENCY_HZ)
        self.declare_parameter("speed", SPEED)

        self.frequency_hz = self.get_parameter("frequency_hz").value
        self.speed = self.get_parameter("speed").value
        self.dt = 1.0 / self.frequency_hz
        self.wheel_angular_velocity = self.speed / WHEEL_RADIUS

        self.joint_pub = self.create_publisher(JointState, "/joint_states", 10)
        self.pose_cov_pub = self.create_publisher(
            PoseWithCovarianceStamped, "/pose_with_covariance", 10
        )
        self.tf_broadcaster = TransformBroadcaster(self)

        self.x = 0.0
        self.wheel_position = 0.0
        self.count = 0

        self.get_logger().info(
            f"TurtleBot3 sim: {self.speed} m/s at {self.frequency_hz} Hz"
        )
        self.timer = self.create_timer(self.dt, self._on_timer)

    def _on_timer(self):
        now = self.get_clock().now().to_msg()

        self.x += self.speed * self.dt
        self.wheel_position += self.wheel_angular_velocity * self.dt

        js = JointState()
        js.header.stamp = now
        js.name = ["wheel_left_joint", "wheel_right_joint"]
        js.position = [self.wheel_position, self.wheel_position]
        js.velocity = [self.wheel_angular_velocity, self.wheel_angular_velocity]
        self.joint_pub.publish(js)

        tf = TransformStamped()
        tf.header.stamp = now
        tf.header.frame_id = "odom"
        tf.child_frame_id = "base_footprint"
        tf.transform.translation.x = self.x
        tf.transform.rotation.w = 1.0
        self.tf_broadcaster.sendTransform(tf)

        t = self.count * self.dt
        sigma_x = 0.02 + 0.01 * t
        sigma_y = 0.01 + 0.005 * t

        cov = [0.0] * 36
        cov[0] = sigma_x**2
        cov[7] = sigma_y**2
        cov[14] = 0.001

        pose_cov = PoseWithCovarianceStamped()
        pose_cov.header.stamp = now
        pose_cov.header.frame_id = "odom"
        pose_cov.pose.pose.position.x = self.x
        pose_cov.pose.pose.orientation.w = 1.0
        pose_cov.pose.covariance = cov
        self.pose_cov_pub.publish(pose_cov)

        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = TurtleBot3Sim()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
