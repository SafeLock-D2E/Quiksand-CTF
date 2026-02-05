#!/bin/bash
set -e

# source ROS2 环境
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash

# 启动 victim 节点（后台）
ros2 run quiksand_lab2 quiksand_node2 &

echo "[*] Quiksand Lab2 node started."

# 进入交互 shell（前台）
exec /bin/bash

