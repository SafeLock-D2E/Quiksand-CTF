import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, ReliabilityPolicy

FLAG = "flag{fake_publisher_takeover}"

class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')

        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.BEST_EFFORT
        )

        self.triggered = False

        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_cb,
            qos
        )

        self.get_logger().info("🛡 monitor_node started, watching /cmd_vel")

    def cmd_cb(self, msg: Twist):
        if self.triggered:
            return

        if abs(msg.linear.x) > 0.1:
            self.triggered = True
            self.get_logger().fatal(f"🏴 FLAG: {FLAG}")

def main():
    rclpy.init()
    node = MonitorNode()
    rclpy.spin(node)
    rclpy.shutdown()
