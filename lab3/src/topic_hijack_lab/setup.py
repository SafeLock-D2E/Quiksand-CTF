from setuptools import find_packages, setup

package_name = 'topic_hijack_lab'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros2',
    maintainer_email='ros2@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'robot_node = topic_hijack_lab.robot_node:main',
            'fake_publisher = topic_hijack_lab.fake_publisher:main',
            'monitor_node = topic_hijack_lab.monitor_node:main',
        ],
    },
)
