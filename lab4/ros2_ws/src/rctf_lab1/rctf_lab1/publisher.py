import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class NormalPublisher(Node):
    def __init__(self):
        super().__init__('publisher')
        
        # 创建一个正常的发布者，使用 RELIABLE 和 KEEP_ALL
        qos_profile = rclpy.qos.QoSProfile(
            reliability=rclpy.qos.ReliabilityPolicy.RELIABLE,
            history=rclpy.qos.HistoryPolicy.KEEP_ALL,
            depth=10
        )
        
        self.publisher = self.create_publisher(String, '/Publisher', qos_profile)
        
        # 每秒钟发布一次消息
        self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = String()
        msg.data = "Move forward"
        
        # 发布消息
        self.publisher.publish(msg)
        
        # 打印日志
        self.get_logger().info(f'Publishing normal message: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = NormalPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
