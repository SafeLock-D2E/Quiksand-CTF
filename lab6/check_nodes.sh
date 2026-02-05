#!/bin/bash

# 设置正确的环境变量
source /opt/ros/jazzy/setup.bash
source /root/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=30
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

echo "=== 检查节点状态 ==="
echo "ROS_DOMAIN_ID: $ROS_DOMAIN_ID"
echo "RMW_IMPLEMENTATION: $RMW_IMPLEMENTATION"
echo ""

echo "=== 节点列表 ==="
ros2 node list
echo ""

echo "=== 话题列表 ==="
ros2 topic list
echo ""

echo "=== 检查 /cpu_load_status 话题 ==="
ros2 topic info /cpu_load_status 2>/dev/null || echo "话题 /cpu_load_status 不存在"
echo ""

echo "=== 检查 /flag 话题 ==="
ros2 topic info /flag 2>/dev/null || echo "话题 /flag 不存在"
echo ""

echo "=== 进程状态 ==="
ps aux | grep python
