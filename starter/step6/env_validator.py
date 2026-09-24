"""
Step 6 - env_validator: checks each reading via /validate_reading, publishes it with the verdict.

    /humidity ----+
                  +--> env_validator --(request)--> /validate_reading
    /temperature -+          |        <-(valid, reason)--+
                             +--> /env/validated   every reading + verdict

Copy to:  ~/ros2_ws/src/env_monitor/env_monitor/env_validator.py
Also:     TODO(6.8) in env_monitor/setup.py
Run:      ros2 run env_monitor env_validator
Check:    ros2 topic echo /env/validated
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

        # TODO(6.4): subscriptions:
        #            'temperature' (Temperature)       -> self.on_temperature
        #            'humidity'    (RelativeHumidity)  -> self.on_humidity
        self.publisher = self.create_publisher(EnvReading, 'env/validated', 10)

        # TODO(6.5): service client, then wait for the server.
        #            API:  self.client = self.create_client(ValidateReading, 'validate_reading')
        #                  while not self.client.wait_for_service(timeout_sec=1.0):
        #                      self.get_logger().info('waiting for /validate_reading')

    def on_humidity(self, msg):
        # TODO(6.4b): store the humidity in percent in self.humidity_pct.
        #             msg.relative_humidity is a fraction, 0.0-1.0.
        pass

    def on_temperature(self, msg):
        # Humidity arrives first, so each temperature completes a reading.
        if self.humidity_pct is None:
            return
        reading = EnvReading()
        reading.stamp = msg.header.stamp
        reading.temperature = msg.temperature
        reading.humidity = self.humidity_pct

        # TODO(6.6): ask the server about msg.temperature.
        #   request = ValidateReading.Request()
        #   request.temperature = msg.temperature
        #   future = self.client.call_async(request)
        #   future.add_done_callback(lambda f: self.on_checked(f, reading))
        # Use call_async here: a blocking call() inside a callback never returns.

    def on_checked(self, future, reading):
        response = future.result()
        # TODO(6.7): set reading.valid and reading.reason from the response, publish EVERY reading,
        #            then log: info when valid, self.get_logger().warn(...) when not.
        _ = (response, reading)  # remove this line when you use them


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
