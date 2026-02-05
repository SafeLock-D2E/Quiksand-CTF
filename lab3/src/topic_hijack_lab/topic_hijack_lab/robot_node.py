import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotNode(Node):
    def __init__(self):
        super().__init__('robot_node')
        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        self.get_logger().info('🤖 Robot started, waiting for /cmd_vel')

    def cmd_vel_callback(self, msg):
        self.get_logger().warn(
            f'🚨 Robot moving! linear.x={msg.linear.x}'
        )

def main():
    rclpy.init()
    node = RobotNode()
    rclpy.spin(node)
    rclpy.shutdown()
