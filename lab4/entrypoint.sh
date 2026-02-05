#!/bin/bash
set -e

echo "[+] RCTF Lab 1 starting..."

# ROS2 基础环境
source /opt/ros/jazzy/setup.bash
source /root/ros2_ws/install/setup.bash

# 靶场配置（攻击面）
export ROS_DOMAIN_ID=30
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

echo "[+] ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
echo "[+] Launching vulnerable publisher..."


# 启动靶场节点
ros2 run rctf_lab1 rctf_lab1_publisher > /dev/null 2>&1 &
ros2 run rctf_lab1 rctf_lab1_subscriber > /dev/null 2>&1 &

exec bash

