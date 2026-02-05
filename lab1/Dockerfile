FROM ros:jazzy-ros-base

WORKDIR /root

# 拷贝工作空间
COPY ros2_ws /root/ros2_ws

# 拷贝 flag
COPY flag /flag

# 拷贝启动脚本
COPY entrypoint.sh /entrypoint.sh

RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && \
    cd /root/ros2_ws && \
    colcon build"
    
COPY motd /etc/motd

RUN echo "cat /etc/motd" >> /root/.bashrc

# 使用启动脚本
ENTRYPOINT ["/entrypoint.sh"]

