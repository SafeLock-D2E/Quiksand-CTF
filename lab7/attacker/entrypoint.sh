#!/bin/bash
set -e

echo "[+] Attacker container ready"
echo "[+] Partial keystore detected"

source /opt/ros/jazzy/setup.bash

export ROS_DOMAIN_ID=30
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

# ⚠️ 注意：这里**不开 Enforce**
# 给选手操作空间（可开 / 可不开 / 可替换）
export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_STRATEGY=Permissive
export ROS_SECURITY_KEYSTORE=/root/keystore

exec bash

