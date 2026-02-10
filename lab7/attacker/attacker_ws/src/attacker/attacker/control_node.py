import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import time


class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')

        self.pub = self.create_publisher(Int32, 'cmd_vel', 10)

        self.get_logger().info('control_node started')

        self.speed = 50
        self.create_timer(1.0, self.attack_loop)

    def attack_loop(self):
        msg = Int32()
        msg.data = self.speed
        self.pub.publish(msg)

        self.get_logger().info(f'Published cmd_vel = {self.speed}')

        # 攻击阶段：逐步升速
        if self.speed < 150:
            self.speed += 10


def main():
    rclpy.init()
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
