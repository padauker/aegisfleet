# AegisFleet

AegisFleet is a modular multi-UAV swarm simulation platform built on ROS2 and Gazebo.
Onboard autonomy is driven by behavior trees, with pluggable search strategies,
coordination algorithms, and mission types. A web-based 3D interface provides live
coverage mapping and fleet telemetry.

---

## Project structure

```
aegisfleet/
├── docker-compose.yml
├── ros2_ws/
│   └── src/
│       ├── aegisfleet_bringup/
│       ├── aegisfleet_dynamics/
│       ├── aegisfleet_search/
│       ├── aegisfleet_coordinator/
│       ├── aegisfleet_mission/
│       ├── aegisfleet_bt/
│       └── aegisfleet_telemetry/
├── sim/
│   └── worlds/
└── web/
    ├── backend/
    └── frontend/
```

---

## Stack

| Layer | Technology |
|---|---|
| Simulation | ROS2 Humble, Gazebo Garden |
| Autonomy | BehaviorTree.CPP v4 |
| Telemetry bridge | FastAPI |
| Frontend | Three.js |
| Environment | Docker Compose |

---

## Architecture

Four plugin axes, each behind an abstract base class:

| Axis | Base class | First implementation |
|---|---|---|
| Dynamics | `dynamics_base.hpp` | `quadrotor_simple` |
| Search strategy | `search_strategy_base.hpp` | `lawnmower` |
| Coordinator | `coordinator_base.hpp` | `centralized_auctioneer` |
| Mission manager | `mission_manager_base.hpp` | `search_and_report` |

Behavior trees (BT.CPP v4, XML-defined) sit between the mission manager and the
dynamics/search layers as the per-UAV decision engine. BT leaf nodes call into
search strategy and dynamics via ROS2 actions and services.

---

## Build order

1. `aegisfleet_dynamics` — `quadrotor_simple` only
2. `aegisfleet_search` — `lawnmower` only
3. `aegisfleet_bt` — `search_and_report.xml` with stub nodes
4. `aegisfleet_bringup` — single UAV launch file

---

## Conventions

- All packages prefixed `aegisfleet_`
- Abstract base classes named `*_base.hpp`, concrete impls in separate `.cpp` files
- BT trees defined in XML under `aegisfleet_bt/trees/`
- No business logic in launch files
- Each plugin axis is independently swappable without touching other modules
- Always use `rclcpp_lifecycle::LifecycleNode` over `rclcpp::Node`
- Prefer ROS2 actions for long-running tasks, services for short queries, topics for telemetry
- BT leaf nodes must be stateless — all state lives in the BT blackboard

---

## Coding standards

- C++17, no exceptions — prefer `std::expected` or status enums for error handling
- Use `const` and `[[nodiscard]]` aggressively
- Do not add ROS2 parameters without a corresponding `.yaml` in `aegisfleet_bringup/config/`

---

## Testing

- One test file per module: `test_<module>.cpp`
- Use `ament_cmake_gtest`
- Every stub test file must include at least one smoke test that instantiates the class

---

## Scaffolding instructions

When scaffolding:
- Create all `CMakeLists.txt`, `package.xml`, and `__init__.py` files for valid ROS2 Humble packages
- Stub all pure virtual interfaces before any concrete implementations
- Do not implement logic unless explicitly asked
- Do not add dependencies not listed in this file without asking
- Do not modify `docker-compose.yml` or `sim/worlds/` unless explicitly asked

A package is complete when it has a valid `package.xml` and `CMakeLists.txt`, all
headers with correct include guards, all pure virtual interfaces stubbed, and a
passing smoke test with no unresolved `TODO` placeholders unless explicitly noted.