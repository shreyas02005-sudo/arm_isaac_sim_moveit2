# Setup on Windows

Replace `WS` with your pixi workspace path (this was developed at `C:\IsaacSim-ros_workspaces\jazzy_ws`).
Keep the path **short**: Windows path-length limits break the build otherwise (NVIDIA's `README_PIXI.md` warns about this).

## 1. Prerequisites

- Windows 11, an NVIDIA GPU with recent drivers (8 GB VRAM worked; Isaac Sim used roughly 4 GB of system memory,
  so close other heavy programs).
- [Pixi](https://pixi.sh) installed.
- Git.
- **Visual Studio Build Tools** with the *Desktop development with C++* workload (developed with the 2026 / v18 version).

## 2. NVIDIA's pixi workspace

Clone NVIDIA's `IsaacSim-ros_workspaces` repository to a short path and follow its `jazzy_ws\README_PIXI.md`:

```cmd
git submodule update --init --recursive
pixi install
```

Its `pixi.toml` provides Isaac Sim (`isaacsim==6.0.1.0`), ROS 2 Jazzy, MoveIt, `rmw_zenoh_cpp` and the tasks used here:
`zenoh` (router) and `sim` (Isaac Sim with the ROS 2 bridge). The environment sets `RMW_IMPLEMENTATION=rmw_zenoh_cpp`.

Always run `cd /d WS` before any `pixi run ...`; pixi fails with `could not find pixi.toml` elsewhere.

## 3. Add the arm packages

1. Copy these packages from your arm workspace into `WS\src\`:
   `my_robot_description`, `my_robot_moveit_config`, `my_robot_bringup`, `my_robot_interfaces`, `my_robot_commander_cpp`.
2. Apply the files in `overlay/` on top (see `overlay/README.md`).
3. Copy `bridge\isaac_trajectory_bridge.py` and `bridge\isaac_arm.launch.xml` to `C:\arm_pkgs\` (or edit the script path
   inside the launch file).

## 4. Build only the arm packages

`pixi run build` builds the whole NVIDIA workspace. For just the arm, open a normal Command Prompt and load the compiler first:

```cmd
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
cd /d WS
pixi run colcon build --merge-install --packages-select my_robot_interfaces my_robot_description my_robot_moveit_config my_robot_bringup my_robot_commander_cpp --cmake-args -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
```

Why those flags:
- `vcvars64.bat`: otherwise `VisualStudioVersion is not set`.
- `-G Ninja`: this colcon does not recognise Visual Studio 18 (`Unknown / unsupported VS version '18.0'`).
- `-DCMAKE_BUILD_TYPE=Release`: Ninja otherwise assumes Debug and fails on a missing `python_d.exe`.

Check: `dir install\share | findstr /i "my_robot"` should list all packages. Open **new** terminals after building.

## 5. Build the Isaac Sim scene

Follow [ISAAC_SCENE.md](ISAAC_SCENE.md) once, then save the scene.

## 6. Run

See the Quick start in the top-level README. Order matters: Zenoh, then Isaac (scene open, **Play**), then the launch, then the commander.

## Optional

- Turn on Windows *Developer Mode* to silence the harmless `Cannot create a symlink to latest log directory` warning.
- The `[system-requirements]` deprecation warning from pixi is harmless.
