from glob import glob

from setuptools import find_packages, setup

package_name = 'dht11_ros'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='asap',
    maintainer_email='asap@todo.todo',
    description='DHT11 temperature and humidity driver (Arduino over USB serial) with a simulator',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'dht11_serial = dht11_ros.serial_node:main',
            'dht11_sim = dht11_ros.sim_node:main',
        ],
    },
)
