data = 'AAB296C4E5094228BA0000EC0000009A2D64'
print(data)


def decode_id(_data):
    x = _data[0:8]
    out = x
    return out


def decode_pressure(_data):
    x = _data[14:16]
    y = _data[12:14]
    out = int(x + y, 16) / 10
    return out


def decode_temp(_data):
    x = _data[10:12]
    y = _data[8:10]
    out = int(x + y, 16) / 100
    return out


def decode_humidity(_data):
    x = _data[14:18]
    out = int(x, 16) % 128
    return out


def decode_voltage(_data):
    x = _data[22:24]
    out = int(x, 16) / 50
    return out


def decode_rssi(_data, _data_length):
    a = _data_length - 4
    b = _data_length - 2
    x = _data[a:b]
    x = int(x, 16)
    out = x * -1
    return out


def decode_snr(_data, _data_length):
    a = _data_length - 2
    b = _data_length
    x = _data[a:b]
    x = int(x, 16)
    out = x / 10
    return int(out)


data_length = len(data)
node_id = decode_id(data)
temp = decode_temp(data)
pressure = decode_pressure(data)
humidity = decode_humidity(data)
voltage = decode_voltage(data)
rssi = decode_rssi(data, data_length)
snr = decode_snr(data, data_length)
print(node_id, temp, pressure, humidity, voltage, rssi, snr)
