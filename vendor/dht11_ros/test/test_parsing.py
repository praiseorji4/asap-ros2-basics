from dht11_ros.parsing import parse_line


def test_reading():
    assert parse_line('T:24.0,H:55.0\r\n') == (24.0, 55.0)


def test_error_line():
    assert parse_line('ERR') is None


def test_garbage():
    assert parse_line('') is None
    assert parse_line('T:abc,H:55') is None
    assert parse_line('\x00\xffT:2') is None
