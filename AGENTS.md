# AGENTS.md

## Project

TurtleBot3 Burger simulation used to exercise
[rewire](https://github.com/rewire-run/rewire) with URDF, TF trees, joint
states, and pose-with-covariance. ROS 2 package name: `rewire_turtlebot3`.
Build type: `ament_python`. Managed with [pixi](https://pixi.sh).

## Layout

```text
rewire_turtlebot3/   # Python package (sim node)
  sim.py             # TurtleBot3Sim node: joint states, TF, pose cov
launch/
  sim.launch.py      # robot_state_publisher + sim
urdf/                # vendored Burger URDF (Apache 2.0, ROBOTIS)
meshes/              # vendored Burger meshes (bases/wheels/sensors)
config/
  rewire.json5       # rewire record config (used by `pixi run viz`)
resource/            # ament package marker
package.xml          # ROS package manifest
setup.py / setup.cfg # ament_python install
pixi.toml               # env, deps, tasks (app / viz)
turtlebot3-example.rbl  # Rerun blueprint (repo root)
assets/                 # README images
```

## Runtime

- Default ROS distro: **jazzy** (`pixi` default environment)
- Other envs: `humble`, `kilted`, `lyrical` via `pixi run -e <env> ...`
- Platforms: `osx-arm64`, `linux-64`
- Channels: conda-forge, robostack-*, prefix.dev/rewire;
  lyrical uses `https://prefix.dev/robostack-lyrical` (not anaconda.org)
- Package build backend: `pixi-build-ros`
- Shares `app` / `viz` task pattern with `camera-example`


### Tasks

| Task | Command |
|------|---------|
| `pixi run app` | `ros2 launch rewire_turtlebot3 sim.launch.py` |
| `pixi run viz` | `rewire record --config $PIXI_PROJECT_ROOT/config/rewire.json5` |

Setup: `pixi install`. Run sim and viz in separate terminals.

### Rewire config (`config/rewire.json5`)

- `app_id`: `turtlebot3-example`
- `diagnostics`: enabled
- Topics: include `/**`, exclude `/rosout` and `/parameter_events`
- Prefer editing this file over hardcoding CLI flags on the `viz` task

## Published topics

| Topic | Type | Source |
|-------|------|--------|
| `/joint_states` | `sensor_msgs/JointState` | `sim` |
| `/pose_with_covariance` | `geometry_msgs/PoseWithCovarianceStamped` | `sim` |
| `/robot_description` | `std_msgs/String` | `robot_state_publisher` |
| `/tf` | `tf2_msgs/TFMessage` | `sim` (`odom` → `base_footprint`) |
| `/tf_static` | `tf2_msgs/TFMessage` | URDF via `robot_state_publisher` |

## Sim behavior (`rewire_turtlebot3/sim.py`)

- Straight-line motion along +x at default `speed=0.05` m/s, `frequency_hz=50`
- Wheel joints: `wheel_left_joint`, `wheel_right_joint` (radius `0.033` m)
- Pose covariance grows over time (x/y variance increases with t)
- Parameters: `frequency_hz`, `speed` (ROS params on node `turtlebot3_sim`)

## Launch (`launch/sim.launch.py`)

1. Load vendored Burger URDF via `xacro` from `rewire_turtlebot3` share
   (`urdf/turtlebot3_burger.urdf`; meshes under `package://rewire_turtlebot3/`)
2. Start `robot_state_publisher` with `robot_description`
3. Start `rewire_turtlebot3` executable `sim`

Console entry point: `sim = rewire_turtlebot3.sim:main` (see `setup.py`).

Description assets are vendored because robostack-lyrical does not publish
`ros-lyrical-turtlebot3-description`. Keep `setup.py` data_files in sync when
adding URDF/meshes.

## Dependencies (runtime)

`rclpy`, `geometry_msgs`, `sensor_msgs`, `std_msgs`, `tf2_ros` /
`tf2_ros_py`, `robot_state_publisher`, `xacro`.
Plus workspace tools: `rewire`, `zenohd`, colcon, ros2cli stack per distro
feature in `pixi.toml`. No external `turtlebot3_description` package.

## Conventions for agents

- Prefer small, focused changes; match existing style (no decorative
  comment dividers, minimal comments unless requested)
- Keep package install paths and entry points in sync across `setup.py`,
  `package.xml`, and `pixi.toml` path package names
  (`ros-<distro>-rewire-turtlebot3`)
- When changing published topics/frames, update README topic table and this
  file
- Do not commit `.pixi/`, `__pycache__/`, `*.egg-info/`, or `files.txt`
- Do not commit `CLAUDE.md` or `.claude/` (if present)
- Git commits: conventional commits (`feat:`, `fix:`, `docs:`, …)
- Markdown lines ≤ 120 characters

## Out of scope

This is a lightweight demo sim, not full Gazebo/Nav2. Do not pull in heavy
simulator stacks unless explicitly requested.
