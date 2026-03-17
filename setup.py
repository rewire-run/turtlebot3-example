import os
from glob import glob

from setuptools import setup

package_name = "rewire_turtlebot3"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (os.path.join("share", package_name), ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    entry_points={
        "console_scripts": [
            "sim = rewire_turtlebot3.sim:main",
        ],
    },
)
