#!/bin/bash
cd ~/ros2_ws
rm -rf build install log
colcon build --symlink-install
source install/setup.bash
source /opt/ros/jazzy/setup.bash
export ROS_SECURITY_KEYSTORE=~/keystore
export ROS_SECURITY_ENABLE=true 
export ROS_SECURITY_STRATEGY=Enforce
ros2 run lab7 victim_node --ros-args --enclave /lab7/victim_node
