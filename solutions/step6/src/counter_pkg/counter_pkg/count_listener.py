"""
Step 4 - count_listener: subscribes to /count (our Count message) and logs who counted what.

Run it:     ros2 run counter_pkg count_listener      (with the counter running in another terminal)
Check it:   the log shows 'heard N from counter'
"""

from asap_interfaces.msg import Count
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class CountListener(Node):
    """A node that listens to the counter."""

    def __init__(self):
        super().__init__('count_listener')
        self.subscription = self.create_subscription(Count, 'count', self.on_count, 10)

    def on_count(self, msg):
        self.get_logger().info(f'heard {msg.count} from {msg.source}')


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
