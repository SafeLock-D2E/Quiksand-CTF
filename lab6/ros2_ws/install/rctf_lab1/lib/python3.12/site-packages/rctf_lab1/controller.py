import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RobotController(Node):
    def __init__(self):
        super().__init__('rctf_lab1_controller')
        self.create_subscription(
            String,
            '/robot_cmd',
            self.cb,
            10
        )

    def cb(self, msg):
        cmd = msg.data.strip()
        self.get_logger().warn(f'[EXECUTE] {cmd}')

        # 🚨 后门：Topic 注入触发
        if cmd == 'GET_FLAG':
            with open('/flag/flag.txt', 'r') as f:
                flag = f.read()
            self.get_logger().error(f'FLAG => {flag}')


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    rclpy.shutdown()
