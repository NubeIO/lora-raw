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
# print(output)
#
# { id: 'AAB296C4',
#   temp: 25.33,
#   pressure: 1030.6,
#   humidity: 58,
#   voltage: 4.72,
#   rssi: -45,
#   snr: 10 }


# let
# data = 'AAB296C4E5094228BA0000EC0000009A2D64'
#
# let
# output = {
#     id: data.substring(0, 8),
#     temp: parseInt(data.substring(10, 12) + data.substring(8, 10), 16) / 100,
#     pressure: parseInt(data.substring(14, 16) + data.substring(12, 14), 16) / 10,
#     humidity: parseInt(data.substring(16, 18), 16) % 128,
#     voltage: parseInt(data.substring(22, 24), 16) / 50,
#     rssi: parseInt(data.substring(data.length - 4, data.length - 2), 16) * -1,
#     snr: parseInt(data.substring(data.length - 2, data.length), 16) / 10,
# };
#
# console.log(output)
#
# let
# sensorType = 'droplet'
# let
# nodeID = 'AAB296C4'.toUpperCase() | | '';
# if (!data) return;
# if (data.length % 2 === 1 & & (data[data.length - 1] == = '\r' | | data[data.length - 1] == = '\n')) {
# data = data.substring(0, data.length - 1);
# } else if (data.substring(data.length - 2, data.length) == = '\r\n') {
# data = data.substring(0, data.length - 2);
# }
# console.log(111)
# if (data.length !=
# = 36 & & data.length != = 44 & & data.substring(2, 4) !== 'AA' & & data.substring(2, 4) != = 'B0' & & data.substring(2, 4) != = 'B1' & & data.substring(2, 4) != = 'B2') return;
# console.log(2222)
#
# if (nodeID == data.substring(0, 8) | | nodeID == '') {
# console.log(3333)
# if (sensorType == = 'microedge' & & data.substring(2, 4) == = 'AA' & & (data.length == = 44 | | data.length == = 36)) {
# console.log('microedge')
#
# // if (this.inputs[0].updated) this.resetWatchdog();
# // this.writeOutputs(this.microEdgeDecode(data));
# } else if ( sensorType == = 'droplet' & & data.substring(2, 3) == = 'B' & & (data.length == = 44 | | data.length == = 36)) {
# console.log('droplet')
# // if (this.inputs[0].updated) this.resetWatchdog();
# // this.writeOutputs(this.dropletDecode(data));
# }
# }
#
#
