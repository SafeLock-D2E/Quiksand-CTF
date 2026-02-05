FROM ros:jazzy-ros-base

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /ros2_ws

COPY ros2_ws/src ./src
COPY entrypoint.sh /entrypoint.sh

RUN . /opt/ros/jazzy/setup.sh && colcon build

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

COPY motd /etc/motd

RUN echo "cat /etc/motd" >> /root/.bashrc

ENTRYPOINT ["/entrypoint.sh"]

