import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String
import time


FLAG = "QuikSand{DDS_PKI_Permission_Hijacking}"


class VictimNode(Node):
    def __init__(self):
        super().__init__('victim_node')

        # speed：每分钟打印次数
        self.speed = 10

        # 订阅控制速度（攻击面）
        self.create_subscription(
            Int32,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # 🚨 对外告警发布（信息外泄点）
        self.alert_pub = self.create_publisher(
            String,
            'alert',
            10
        )

        self.get_logger().info(
            'victim_node started (secure mode). Waiting for cmd_vel...'
        )

        self.last_print_time = time.time()
        self.create_timer(0.1, self.work_loop)

    def cmd_vel_callback(self, msg: Int32):
        self.speed = msg.data
        self.get_logger().info(f'[cmd_vel] speed updated to {self.speed}')

    def work_loop(self):
        if self.speed <= 0:
            return

        # ===== 告警 & FLAG 泄露逻辑 =====
        if self.speed > 100:
            self.get_logger().warn('!!! SPEED LIMIT EXCEEDED !!!')

            # 本地打印
            self.get_logger().warn(f'FLAG => {FLAG}')

            # 🚨 持续对外发布
            alert_msg = String()
            alert_msg.data = (
                '[ALERT] SPEED LIMIT EXCEEDED | '
                f'FLAG={FLAG}'
            )
            self.alert_pub.publish(alert_msg)

        interval = 60.0 / self.speed
        now = time.time()

        if now - self.last_print_time >= interval:
            self.last_print_time = now
            self.get_logger().info('Victim is working...')


def main():
    rclpy.init()
    node = VictimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
