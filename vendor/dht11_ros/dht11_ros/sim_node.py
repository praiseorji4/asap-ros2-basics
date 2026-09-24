"""
dht11_sim: simulated DHT11, with the same topics and types as dht11_serial.

    humidity      sensor_msgs/msg/RelativeHumidity   (0.0-1.0, as the message defines it)
    temperature   sensor_msgs/msg/Temperature        (degrees Celsius)

The temperature moves towards target_temperature by at most 0.5 C per reading.
A fraction of readings (glitch_rate) are NaN (failed read).

Parameters: rate_hz (1.0), target_temperature (27.0, changeable live),
glitch_rate (0.05, changeable live), base_humidity (60.0 %), frame_id (dht11).
"""

import math
import random

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import RelativeHumidity, Temperature


class Dht11Sim(Node):
    """Temperature that follows a settable target, wandering humidity, occasional failed reads."""

    def __init__(self) -> None:
        super().__init__('dht11_sim')
        rate_hz = self.declare_parameter('rate_hz', 1.0).value
        self.temperature = self.declare_parameter('target_temperature', 27.0).value
        self.declare_parameter('glitch_rate', 0.05)
        self.humidity = self.declare_parameter('base_humidity', 60.0).value
        self.frame_id = self.declare_parameter('frame_id', 'dht11').value

        self.temp_pub = self.create_publisher(Temperature, 'temperature', 10)
        self.hum_pub = self.create_publisher(RelativeHumidity, 'humidity', 10)
        self.create_timer(1.0 / rate_hz, self.tick)
        self.get_logger().info('simulated DHT11 running (no hardware needed)')

    def tick(self) -> None:
        """Take one fake reading and publish it."""
        target = self.get_parameter('target_temperature').value
        step = min(max(target - self.temperature, -0.5), 0.5)
        # Stay within the DHT11's range: 0-50 C, 20-90 % RH.
        self.temperature = min(max(self.temperature + step + random.gauss(0.0, 0.1), 0.0), 50.0)
        self.humidity = min(max(self.humidity + random.gauss(0.0, 0.5), 20.0), 90.0)
        temperature_c = round(self.temperature, 1)
        humidity_pct = round(self.humidity, 1)

        if random.random() < self.get_parameter('glitch_rate').value:
            temperature_c = math.nan  # a failed read

        stamp = self.get_clock().now().to_msg()
        hum = RelativeHumidity()
        hum.header.stamp = stamp
        hum.header.frame_id = self.frame_id
        hum.relative_humidity = humidity_pct / 100.0
        self.hum_pub.publish(hum)

        temp = Temperature()
        temp.header.stamp = stamp
        temp.header.frame_id = self.frame_id
        temp.temperature = temperature_c
        self.temp_pub.publish(temp)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = Dht11Sim()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
