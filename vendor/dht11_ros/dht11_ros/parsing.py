"""
Parse the text lines the dht11_serial Arduino sketch prints.

The sketch prints one line every two seconds:

    T:24.0,H:55.0     temperature in degrees C, relative humidity in percent
    ERR               the sensor did not answer this time
"""

from typing import Optional, Tuple


def parse_line(line: str) -> Optional[Tuple[float, float]]:
    """Return (temperature_c, humidity_percent), or None if the line is not a reading."""
    line = line.strip()
    if not line.startswith('T:') or ',H:' not in line:
        return None
    t_part, h_part = line[2:].split(',H:', 1)
    try:
        return float(t_part), float(h_part)
    except ValueError:
        return None
