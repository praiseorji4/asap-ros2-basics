"""
Step 3 - count_listener: subscribes to /count and logs every number it hears.

Run it:     ros2 run counter_pkg count_listener      (with the counter running in another terminal)
Check it:   rqt_graph   shows  /counter -> /count -> /count_listener
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32


class CountListener(Node):
    """A node that listens to the counter."""

    def __init__(self):
        super().__init__('count_listener')
        # Type and topic name must match the publisher.
        self.subscription = self.create_subscription(Int32, 'count', self.on_count, 10)

    def on_count(self, msg):
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
