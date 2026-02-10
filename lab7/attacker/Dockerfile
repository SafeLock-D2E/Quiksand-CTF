FROM ros:jazzy-ros-base

WORKDIR /root

RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# 给攻击者一个 workspace（参考答案在宿主机，不默认构建）
RUN mkdir -p /root/attacker_ws/src

# 拷贝“泄露的 keystore”
COPY keystore /root/keystore

# motd
COPY motd /etc/motd
RUN echo "cat /etc/motd" >> /root/.bashrc

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

