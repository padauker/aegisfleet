import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('aegisfleet_bringup')

    world_path  = os.path.join(pkg, 'worlds', 'aegisfleet_base.sdf')
    model_path  = os.path.join(pkg, 'models')
    bridge_yaml = os.path.join(pkg, 'config', 'bridge.yaml')

    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=model_path
    )

    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', world_path, '-r'],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        parameters=[{
            'config_file': bridge_yaml,
            'use_sim_time': True,
        }],
        output='screen'
    )

    return LaunchDescription([
        set_gz_resource_path,
        gz_sim,
        bridge,
    ])