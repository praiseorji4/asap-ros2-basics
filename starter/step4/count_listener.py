"""
Step 4 - count_listener: subscribes to asap_interfaces/msg/Count on /count.

Copy to:  ~/ros2_ws/src/counter_pkg/counter_pkg/count_listener.py
Run:      ros2 run counter_pkg count_listener
Check:    listener logs 'heard N from counter'
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32

# TODO(4.5a): import Count from asap_interfaces.msg


class CountListener(Node):
    """A node that listens to the counter."""

    def __init__(self):
        super().__init__('count_listener')
        # TODO(4.5b): subscribe with Count instead of Int32.
        self.subscription = self.create_subscription(Int32, 'count', self.on_count, 10)

    def on_count(self, msg):
        # TODO(4.5c): log msg.count and msg.source (a Count has no .data).
        self.get_logger().info(f'heard {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = CountListener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
