import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class NormalPublisher(Node):
    def __init__(self):
        super().__init__('rctf_lab1_normal_pub')
        self.pub = self.create_publisher(String, '/robot_cmd', 10)
        self.create_timer(1.0, self.send)

    def send(self):
        msg = String()
        msg.data = f"Hello ROS2 | FLAG={open('/flag/flag.txt').read().strip()}"
        self.pub.publish(msg)
        self.get_logger().info('[NORMAL] MOVE_FORWARD')


def main(args=None):
    rclpy.init(args=args)
    node = NormalPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
