FROM ros:jazzy-ros-base

WORKDIR /root/ros2_ws

RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

COPY src src
COPY keystore /root/keystore

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

