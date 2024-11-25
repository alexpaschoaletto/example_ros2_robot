import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # este script executa o nó do robô, com
    # a descrição física do mesmo dentro da
    # pasta 'description'. Altere as variáveis
    # abaixo caso a estrutura do projeto também
    # seja alterada.

    description_folder = 'description'
    robot_name = 'robot_main'
    robot_description_file = 'main.urdf.xacro'

    xacro_file = os.path.join(
        get_package_share_directory(robot_name),
        description_folder,
        robot_description_file
    )
    

    robot_description = xacro.process_file(xacro_file).toxml()
    use_sim_time = LaunchConfiguration('use_sim_time')
    

    robot = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time
        }]
    )


    default_args = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use sim time if true'
    )


    return LaunchDescription([
        default_args,
        robot
    ])
