FROM ros:jazzy-ros-base

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DOMAIN_ID=0

WORKDIR /root/lab3

# 拷贝整个 ROS 2 workspace（保持结构不变）
COPY . /root/lab3
COPY motd /etc/ctf_motd
# 安装 colcon
RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# 在容器内重新编译（不要用宿主机的 build）
RUN rm -rf build install log && \
    /bin/bash -c "source /opt/ros/jazzy/setup.bash && colcon build"

# 启动脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

