import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
import time
import random

# 尝试导入 fastdds，如果不可用则使用模拟实现
try:
    from fastdds import dds
    HAS_FASTDDS = True
except ImportError:
    HAS_FASTDDS = False
    print("fastdds-python not found, using simulated implementation")


class DDSParticipantManager:
    """DDS 参与者管理器"""
    
    def __init__(self):
        self.participants = []
        self.factory = None
        self.initialize()
    
    def initialize(self):
        """初始化 DDS 工厂"""
        if HAS_FASTDDS:
            try:
                self.factory = dds.DomainParticipantFactory.get_instance()
            except Exception as e:
                print(f"Failed to initialize DDS factory: {e}")
                self.factory = None
    
    def create_participant(self, domain_id=0):
        """创建一个 DDS 参与者"""
        if not HAS_FASTDDS or not self.factory:
            # 模拟实现：消耗一些 CPU 时间
            start = time.time()
            while time.time() - start < 0.05:  # 模拟创建参与者的 CPU 消耗
                pass
            return True
        
        try:
            qos = dds.DomainParticipantQos()
            qos.name(f"Participant_{random.randint(1, 1000000)}")
            participant = self.factory.create_participant(domain_id, qos)
            
            if participant:
                self.participants.append(participant)
                return True
            return False
        except Exception as e:
            print(f"Error creating participant: {e}")
            return False
    
    def get_participant_count(self):
        """获取当前参与者数量"""
        return len(self.participants)


class CpuLoadGeneratorNode(Node):
    """CPU 负载生成节点"""
    
    def __init__(self):
        super().__init__('cpu_load_generator')
        
        # 控制标志（先初始化，确保线程安全）
        self.running = True
        self.create_participants = False
        
        # 创建发布者，用于报告状态
        self.publisher = self.create_publisher(String, '/cpu_load_status', 10)
        
        # 配置参数
        self.declare_parameter('target_cpu_percent', 50.0)
        self.declare_parameter('participants_batch_size', 10)
        self.declare_parameter('check_interval', 1.0)
        
        # 获取参数值
        self.target_cpu = self.get_parameter('target_cpu_percent').value
        self.batch_size = self.get_parameter('participants_batch_size').value
        self.check_interval = self.get_parameter('check_interval').value
        
        # 初始化 DDS 参与者管理器
        self.participant_manager = DDSParticipantManager()
        
        # 状态变量
        self.current_participants = 0
        self.adjustment_rate = 0.5  # 调整速率，避免振荡
        
        # 创建定时器，定期检查和调整 CPU 负载
        self.timer = self.create_timer(self.check_interval, self.adjust_cpu_load)
        
        # 创建线程用于创建参与者
        self.worker_thread = threading.Thread(target=self.worker_loop, daemon=True)
        self.worker_thread.start()
        
        self.get_logger().info(f"CPU Load Generator node started")
        self.get_logger().info(f"Target CPU usage: {self.target_cpu}%")
        self.get_logger().info(f"Using {'real DDS' if HAS_FASTDDS else 'simulated DDS'} implementation")
    
    def get_current_cpu_usage(self):
        """获取当前 CPU 使用率"""
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            # 模拟实现：返回随机值（仅用于演示）
            return random.uniform(0, 100)
    
    def worker_loop(self):
        """工作线程循环，用于创建参与者"""
        while self.running:
            if self.create_participants:
                # 批量创建参与者
                for _ in range(self.batch_size):
                    self.participant_manager.create_participant()
                    self.current_participants += 1
                self.create_participants = False
            time.sleep(0.1)
    
    def adjust_cpu_load(self):
        """调整 CPU 负载"""
        if not self.running:
            return
            
        current_cpu = self.get_current_cpu_usage()
        cpu_diff = current_cpu - self.target_cpu
        
        # 创建状态消息
        msg = String()
        
        if abs(cpu_diff) < 5.0:
            # CPU 负载在目标范围内
            participant_count = self.participant_manager.get_participant_count()
            status = f"CPU: {current_cpu:.1f}% (Target: {self.target_cpu}%) - Stable - Participants: {participant_count}"
            msg.data = status
            self.get_logger().info(status)
        elif cpu_diff < 0:
            # CPU 负载低于目标，需要创建更多参与者
            deficit = self.target_cpu - current_cpu
            # 根据差距计算需要创建的参与者批次
            batches_needed = max(1, int(deficit / 10))
            
            status = f"CPU: {current_cpu:.1f}% (Target: {self.target_cpu}%) - Creating {batches_needed * self.batch_size} more participants"
            msg.data = status
            self.get_logger().info(status)
            
            # 触发创建参与者
            for _ in range(batches_needed):
                self.create_participants = True
                time.sleep(self.adjustment_rate)
        else:
            # CPU 负载高于目标，暂时不做处理（不删除参与者）
            participant_count = self.participant_manager.get_participant_count()
            status = f"CPU: {current_cpu:.1f}% (Target: {self.target_cpu}%) - Above target - Participants: {participant_count}"
            msg.data = status
            self.get_logger().info(status)
        
        # 发布状态消息
        self.publisher.publish(msg)
    
    def destroy_node(self):
        """销毁节点时的处理（不清除参与者）"""
        self.get_logger().info("Shutting down CPU load generator node...")
        
        # 停止运行标志，不再生成新的参与者
        self.running = False
        
        # 等待工作线程结束
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2.0)
        
        # 取消定时器
        if self.timer:
            self.timer.cancel()
        
        # 不清除参与者，保持 CPU 占用
        
        participant_count = self.participant_manager.get_participant_count()
        self.get_logger().info(f"Node shutdown complete. {participant_count} participants remain active.")
        
        super().destroy_node()


def main(args=None):
    # 检查是否已经初始化
    if not rclpy.ok():
        rclpy.init(args=args)
    
    node = CpuLoadGeneratorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        # 只在必要时调用 shutdown
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()