import os
from glob import glob

from setuptools import setup

package_name = "turtlebot3"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
    ],
    install_requires=["setuptools"],
    entry_points={
        "console_scripts": [
            "sim = turtlebot3.sim:main",
        ],
    },
)
