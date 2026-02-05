#!/bin/bash
set -e

echo

cat /etc/ctf_motd

echo "[+] Starting ROS 2 Topic Hijack Lab (Docker)"

# 1. 删除源码（最关键）
rm -rf /root/lab3/src
rm -rf /root/lab3/Dockerfile
rm -rf /root/lba3/README.md

rm -rf /root/lab3/build /root/lab3/log

# ROS 2 环境
source /opt/ros/jazzy/setup.bash
source /root/lab3/install/setup.bash

# 启动 robot（后台）
ros2 run topic_hijack_lab robot_node &
ROBOT_PID=$!

# 启动 monitor（后台）
ros2 run topic_hijack_lab monitor_node &
MONITOR_PID=$!

echo "[+] robot_node started (pid=$ROBOT_PID)"
echo "[+] monitor_node started (pid=$MONITOR_PID)"
echo "[+] Container is ready. Dropping to shell."

# 把前台交给 bash（关键）
exec bash

