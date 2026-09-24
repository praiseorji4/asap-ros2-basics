# Start the DHT11 driver: the real one (mode:=serial) or the simulated one (mode:=sim).
#
#   ros2 launch dht11_ros dht11.launch.py                                   # simulated
#   ros2 launch dht11_ros dht11.launch.py mode:=serial port:=/dev/ttyACM0   # real Arduino

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import EqualsSubstitution, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    mode = LaunchConfiguration('mode')
    return LaunchDescription([
        DeclareLaunchArgument('mode', default_value='sim', choices=['sim', 'serial'],
                              description='sim: no hardware; serial: Arduino on a USB port'),
        DeclareLaunchArgument('port', default_value='/dev/ttyACM0',
                              description='serial port of the Arduino (mode:=serial only)'),
        DeclareLaunchArgument('target_temperature', default_value='27.0',
                              description='temperature the sim drifts towards (mode:=sim only)'),
        DeclareLaunchArgument('glitch_rate', default_value='0.05',
                              description='fraction of failed (NaN) readings (mode:=sim only)'),
        Node(package='dht11_ros', executable='dht11_sim', output='screen',
             parameters=[{'glitch_rate': LaunchConfiguration('glitch_rate'),
                          'target_temperature': LaunchConfiguration('target_temperature')}],
             condition=IfCondition(EqualsSubstitution(mode, 'sim'))),
        Node(package='dht11_ros', executable='dht11_serial', output='screen',
             parameters=[{'port': LaunchConfiguration('port')}],
             condition=IfCondition(EqualsSubstitution(mode, 'serial'))),
    ])
