import subprocess
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    urdf_path = (
        Path(get_package_share_directory("rewire_turtlebot3"))
        / "urdf"
        / "turtlebot3_burger.urdf"
    )

    urdf = subprocess.run(
        [
            "xacro",
            str(urdf_path),
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
                package="rewire_turtlebot3",
                executable="sim",
            ),
        ]
    )
