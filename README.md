<h1 align="center">
  <a href="https://rewire.run/">
    <img alt="rewire" src="https://rewire.run/brand/rewire-banner.png">
  </a>
</h1>

<p align="center">
  <a href="https://pixi.sh">
    <img alt="Pixi Badge" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json"/>
  </a>
</p>

TurtleBot3 Burger simulation for testing [rewire](https://github.com/rewire-run/rewire) with URDF, TF trees,
joint states, and pose with covariance.

## Topics

| Topic | Type | Description |
|---|---|---|
| `/joint_states` | `sensor_msgs/JointState` | Wheel joint positions and velocities |
| `/pose_with_covariance` | `geometry_msgs/PoseWithCovarianceStamped` | Pose with growing uncertainty |
| `/robot_description` | `std_msgs/String` | URDF from `robot_state_publisher` |
| `/tf` | `tf2_msgs/TFMessage` | Dynamic transform: `odom` → `base_footprint` |
| `/tf_static` | `tf2_msgs/TFMessage` | Static transforms from URDF |

## Environments

| Environment | ROS distro |
|-------------|------------|
| `default` / `jazzy` | Jazzy |
| `humble` | Humble |
| `kilted` | Kilted |
| `lyrical` | Lyrical |

The Burger URDF and meshes are vendored in this package (from ROBOTIS
`turtlebot3_description`, Apache 2.0), so no external
`turtlebot3_description` package is required — including on Lyrical, where
robostack does not publish it yet.

## Setup

Requires [pixi](https://pixi.sh).

```bash
pixi install
```

## Usage

```bash
pixi run app
```

In a separate terminal, run rewire to visualize in Rerun:

```bash
pixi run viz
```

`app` launches `sim.launch.py`. `viz` runs `rewire record` with
[`config/rewire.json5`](config/rewire.json5) (all topics except `/rosout` and `/parameter_events`).
Add `-e <env>` to pick a ROS 2 distro other than the default (jazzy):

```bash
pixi run -e humble app
pixi run -e kilted app
pixi run -e lyrical app
```

## How it works

The launch file starts two nodes:

- **robot_state_publisher** — publishes the vendored TurtleBot3 Burger URDF and static TF tree
- **sim** — drives the robot in a straight line, publishing joint states, dynamic TF, and pose with
  covariance (uncertainty grows over time)
