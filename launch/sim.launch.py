import subprocess

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    urdf = subprocess.run(
        [
            "xacro",
            "/opt/ros/humble/share/turtlebot3_description/urdf/turtlebot3_burger.urdf",
            "namespace:=/",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    return LaunchDescription(
        [
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": urdf}],
            ),
            Node(
                package="turtlebot3",
                executable="sim",
            ),
        ]
    )
