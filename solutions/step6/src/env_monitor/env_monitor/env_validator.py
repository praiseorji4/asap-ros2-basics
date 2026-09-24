"""
Step 6 - env_validator: checks each reading via /validate_reading, publishes it with the verdict.

Subscribes: /temperature (sensor_msgs/Temperature), /humidity (sensor_msgs/RelativeHumidity)
Calls:      /validate_reading (asap_interfaces/srv/ValidateReading)
Publishes:  /env/validated (asap_interfaces/msg/EnvReading) - every reading, with valid + reason

Run it:     ros2 run env_monitor env_validator     (needs dht11_ros and validator_server running)
Check it:   ros2 topic echo /env/validated
"""

from asap_interfaces.msg import EnvReading
from asap_interfaces.srv import ValidateReading
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import RelativeHumidity, Temperature


class EnvValidator(Node):
    """Sensor in, service check, reading + verdict out."""

    def __init__(self):
        super().__init__('env_validator')
        self.humidity_pct = None  # latest humidity, in percent

        self.create_subscription(Temperature, 'temperature', self.on_temperature, 10)
        self.create_subscription(RelativeHumidity, 'humidity', self.on_humidity, 10)
        self.publisher = self.create_publisher(EnvReading, 'env/validated', 10)

        self.client = self.create_client(ValidateReading, 'validate_reading')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for /validate_reading (is validator_server running?)')
        self.get_logger().info('connected to /validate_reading')

    def on_humidity(self, msg):
        # sensor_msgs/RelativeHumidity is a fraction, 0.0-1.0. EnvReading carries percent.
        self.humidity_pct = msg.relative_humidity * 100.0

    def on_temperature(self, msg):
        # Humidity arrives first, so each temperature completes a reading.
        if self.humidity_pct is None:
            return
        reading = EnvReading()
        reading.stamp = msg.header.stamp
        reading.temperature = msg.temperature
        reading.humidity = self.humidity_pct

        request = ValidateReading.Request()
        request.temperature = msg.temperature
        # A blocking call() inside a callback never returns; use call_async.
        future = self.client.call_async(request)
        future.add_done_callback(lambda f: self.on_checked(f, reading))

    def on_checked(self, future, reading):
        response = future.result()
        reading.valid = response.valid
        reading.reason = response.reason
        # Publish every reading, valid or not.
        self.publisher.publish(reading)
        if reading.valid:
            self.get_logger().info(
                f'ok       {reading.temperature:.1f} C  {reading.humidity:.1f} %')
        else:
            self.get_logger().warn(f'NOT OK   {reading.reason}')


def main(args=None):
    rclpy.init(args=args)
    node = EnvValidator()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
