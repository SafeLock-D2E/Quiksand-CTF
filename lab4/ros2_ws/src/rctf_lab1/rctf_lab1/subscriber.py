import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class QoS_Subscriber(Node):
    def __init__(self):
        super().__init__('subscriber')
        
        self.subscription = self.create_subscription(
            String,
            '/Publisher',
            self.listener_callback,
            10
        )
        
        # 创建发布者，用于返回信息
        self.publisher = self.create_publisher(String, '/SubscriberResponse', 10)
        
        # 用来检测丢包的计时器
        self.last_msg_time = time.time()
        self.missed_msgs = 0

    def listener_callback(self, msg):
        current_time = time.time()

        # 检查是否发生丢包：如果收到消息的时间间隔大于某个阈值，认为发生了丢包
        if current_time - self.last_msg_time > 0.5:  # 0.5秒钟没收到消息，认为丢包
            self.missed_msgs += 1

        # 更新接收到消息的时间
        self.last_msg_time = current_time

        self.get_logger().info(f'Received message: "{msg.data}"')
        
        # 创建返回消息
        response_msg = String()
        
        # 如果丢包次数大于 1，返回 flag
        if self.missed_msgs > 1:
            response_msg.data = f'FLAG => flag{{Quiksand_lab4_downgrade_004}}'
            self.get_logger().error(f'FLAG => flag{{Quiksand_lab4_downgrade_004}}')
            self.missed_msgs = 0  # 重置丢包计数
        else:
            # 否则返回当前时间
            response_msg.data = f'Current time: {current_time}'
        
        # 发布返回消息
        self.publisher.publish(response_msg)
        self.get_logger().info(f'Response sent: "{response_msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = QoS_Subscriber()
    rclpy.spin(node)
    rclpy.shutdown()
