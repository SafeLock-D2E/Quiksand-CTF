#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class HiddenParamNode(Node):
    def __init__(self):
        super().__init__('quiksend_node2')

        # 声明一个“系统风格”的隐藏参数
        self.declare_parameter(
            'sys.runtime.seed',
            'flag{Quiksand_lab2_discovery_leak_002}'
        )

        self.get_logger().info('Hidden param node started.')

def main(args=None):
    rclpy.init(args=args)
    node = HiddenParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

