# 🏜️ Quiksand-CTF

> 一个面向 **机器人系统（ROS / ROS2）安全** 的实战型 CTF 靶场  
> 聚焦「信息流砂化（Quiksand Information Flow）」与真实机器人攻击面

---

## 📌 项目简介

**Quiksand-CTF** 是一个专注于 **机器人与自动化系统安全** 的 CTF 题目平台，  
通过可运行的 ROS / ROS2 场景，模拟真实机器人系统中：

- 信息泄露
- 隐蔽通信
- 异常话题流（Topic）
- 节点行为伪装
- 指令劫持与状态污染

攻击面并非“显眼漏洞”，而是像 **流砂（Quiksand）一样** ——  
**看似正常，实则越陷越深。**

---

## 🎯 设计理念（Quiksand Philosophy）

传统靶场：  
> “漏洞在这里，你看得见”

Quiksand-CTF：  
> “一切都在正常运行，但你已经被利用了”

核心理念：

- ✅ **系统功能正常**
- ✅ **Topic / Node 看似合理**
- ❌ **信息在不知不觉中被泄露或操控**

---

## 🧠 覆盖的安全场景

- ROS / ROS2 Topic 信息泄露
- 隐藏节点与伪装通信
- 非显式异常的数据外流
- 机器人状态被悄然篡改
- 安全监控失效但系统未报错

---

## 🧪 当前靶场结构（示例）
Quiksand-CTF/
├── lab1/ # 基础信息泄露靶场
├── lab2/ # 流砂信息流靶场（隐蔽 Topic）
├── docker/ # Docker 环境
├── docs/ # 题目说明与解题思路
└── README.md


---

## 🧩 示例靶场说明（Lab2）

**场景特点：**

- Topic 可以被 `ros2 topic list` 列出
- 数据内容表面“正常”
- 实际包含：
  - 编码信息
  - 状态泄露
  - 非预期控制信号

**挑战点：**

- ❓ 为什么“能看到 Topic ≠ 安全”
- ❓ 如何判断 Topic 是否在 **侧信道通信**
- ❓ 如何区分“正常业务数据”与“攻击载荷”

---

## 🚀 快速开始

### 1️⃣ 克隆项目

```bash
git clone https://github.com/SafeLock-D2E/Quiksand-CTF.git
cd Quiksand-CTF
```

### 2️⃣ 启动 Docker 靶场（示例）
```bash
docker compose up -d
docker build -t  <<Damaged container>> .
```


### 3️⃣ 进入攻击或受害容器
```bash
docker exec -it <<CONTAINER ID >> bash
docker run   -it <<Damaged container>>  .
```

### 🛠️ 适合人群

机器人安全研究人员
ROS / ROS2 开发者
工控 / 自动化安全工程师
CTF 选手（进阶）
做机器人安全教学 / 培训的团队

### ⚠️ 使用声明
本项目 仅用于学习、研究与教学目的
❌ 禁止用于任何未授权攻击
❌ 禁止用于生产系统
❌ 作者不承担任何滥用责任

### 🧭 未来计划

 更高级的隐蔽通信靶场
 ROS2 DDS 层攻击题
 机器人行为级异常检测题
 自动化评分与 Flag 校验
 红蓝对抗模式
 
🤝 贡献方式

欢迎：
提交新的靶场
改进题目设计
修复环境问题

提出更“阴”的攻击思路 😈
请直接提交 PR 或 Issue。

🧠 作者 & 项目背景
本项目由 QuikSand流砂信息科技 发起，
关注 机器人系统、智能设备与高价值目标的真实安全风险。

如果你觉得这个项目有点“危险”，
那说明它做对了。

⭐ Star 一下

如果你觉得这个项目对你有帮助，
欢迎 Star ⭐ 支持我们继续把坑挖深一点。