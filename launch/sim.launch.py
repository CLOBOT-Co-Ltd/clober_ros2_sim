#!/usr/bin/env python3
#
# Copyright 2022 CLOBOT Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # gazebo launch #
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            pkg_gazebo_ros, 'launch', 'gazebo.launch.py'))
    )

    world_path = os.path.join(get_package_share_directory(
        'clober_ros2_sim'), 'worlds', 'suntech_lift.world')

    world_model_path = os.path.join(
        get_package_share_directory('clober_ros2_sim'), 'models')
    robot_description_path = os.path.join(
        get_package_share_directory('clober_description'), 'launch')

    os.environ["GAZEBO_MODEL_PATH"] = world_model_path

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gzserver', world_path,
                 '-s', 'libgazebo_ros_init.so',
                 '-s', 'libgazebo_ros_factory.so',
                 '--verbose'],
            output='screen'
        ),

        ExecuteProcess(
            cmd=['gzclient'],
            output='screen'
        ),

        ExecuteProcess(
            cmd=['ros2', 'run', 'gazebo_ros', 'spawn_entity.py', '-file', world_model_path+'/clober/'+'model.sdf',
                 '-entity', 'clober', '-spawn_service_timeout', '300', '-x', '3.0', '-y', '-3.0', '-z', '0.1'],
            output='screen'
        ),

        IncludeLaunchDescription(PythonLaunchDescriptionSource([
            robot_description_path, '/description_launch.py'
        ]), launch_arguments={'use_sim_time': use_sim_time}.items(),
        )
    ])
