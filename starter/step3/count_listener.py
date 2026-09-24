"""
Step 3 - count_listener: subscribes to /count and logs every number.

Copy to:  ~/ros2_ws/src/counter_pkg/counter_pkg/count_listener.py
Also:     TODO(3.6) in setup.py, TODO(3.7) in package.xml
Run:      ros2 run counter_pkg count_listener
Check:    rqt_graph   /counter -> /count -> /count_listener
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32


class CountListener(Node):
    """A node that listens to the counter."""

    def __init__(self):
        super().__init__('count_listener')
        # TODO(3.4): subscribe to 'count' (Int32); call self.on_count for each message.
        #            API:  self.subscription = self.create_subscription(
        #                      <type>, '<topic>', <callback>, 10)

    def on_count(self, msg):
        # TODO(3.5): log msg.data
        #            API:  self.get_logger().info(f'heard {msg.data}')
        pass


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
