import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import subprocess
import re

class CpuMonitorNode(Node):
    def __init__(self):
        super().__init__('cpu_monitor')
        
        # 创建发布者，发布到 /flag 话题
        self.publisher = self.create_publisher(String, '/flag', 10)
        
        # 创建定时器，定期检查 CPU 使用情况
        self.timer = self.create_timer(1.0, self.check_cpu_usage)
        
        self.get_logger().info('CPU monitor node started')
    
    def check_cpu_usage(self):
        """检查系统 CPU 总使用率"""
        try:
            # 使用 top 命令获取 CPU 使用情况
            result = subprocess.run(['top', '-b', '-n', '1'], 
                                  capture_output=True, text=True)
            
            # 解析 top 命令输出，获取整体 CPU 使用率
            output = result.stdout
            lines = output.split('\n')
            
            # 标志，指示是否发现高 CPU 使用率
            high_cpu_found = False
            total_cpu_usage = 0.0
            
            # 查找 CPU 使用率摘要行
            for line in lines:
                # 查找符合 CPU 使用率摘要行格式的行
                match = re.search(r'%Cpu\(s\):\s+.*?(\d+\.\d+)\s+id', line)
                if match:
                    idle_cpu = float(match.group(1))
                    total_cpu_usage = 100.0 - idle_cpu
                    self.get_logger().info(f'Total CPU usage: {total_cpu_usage:.2f}%')
                    
                    if total_cpu_usage > 50.0:
                        high_cpu_found = True
                    break
            
            # 创建消息
            msg = String()
            
            if high_cpu_found:
                # 如果 CPU 总使用率超过 50%，发布 flag
                msg.data = 'flag{Quiksand_lab6_discovery_leak_006}'
                self.get_logger().info(f'Publishing flag: flag{{Quiksand_lab6_discovery_leak_006}} (Total CPU usage: {total_cpu_usage:.2f}%)')
            else:
                # 否则发布正常消息
                msg.data = f'No high CPU usage detected (Total: {total_cpu_usage:.2f}%)'
            
            # 发布消息
            self.publisher.publish(msg)
            
        except Exception as e:
            self.get_logger().error(f'Error checking CPU usage: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = CpuMonitorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()