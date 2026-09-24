"""
Step 3 - counter: counts up once a second and publishes the number on /count.

Run it:     ros2 run counter_pkg counter
Check it:   ros2 topic echo /count
            ros2 topic hz /count
            ros2 interface show std_msgs/msg/Int32
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32


class Counter(Node):
    """A node that counts and publishes the count."""

    def __init__(self):
        super().__init__('counter')
        self.count = 0
        # (type, topic, queue depth)
        self.publisher = self.create_publisher(Int32, 'count', 10)
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.count += 1
        msg = Int32()
        msg.data = self.count
        self.publisher.publish(msg)
        self.get_logger().info(f'published {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = Counter()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
