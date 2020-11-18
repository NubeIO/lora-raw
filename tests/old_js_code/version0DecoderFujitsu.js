let data = "C1AB289500B608B4273005DB37234470"
// "79ABEA6B00ED07B6273C05DD37FB6A70
// "53ABF5DF003706B6275005DC37CC4F70
// "8AAB1284001C08B8273B03DD37EE6373
// "6CAB113100C708AC272B0BD137657673





var hexString = data

nodeId = hexString.substring(0, 8);
orient = parseInt("0x" + hexString.substring(8, 10));
temp = parseInt("0x" + hexString.substring(12, 14) + hexString.substring(10, 12)) / 100;
pressure = parseInt("0x" + hexString.substring(16, 18) + hexString.substring(14, 16)) / 10;
humidity = parseInt("0x" + hexString.substring(18, 20)) % 128;
movement = parseInt("0x" + hexString.substring(18, 20)) > 127 ? true : false;
light = Math.pow(parseInt("0x" + hexString.substring(20, 22)), 2);
voltage = parseInt("0x" + hexString.substring(22, 24)) / 50;
rssi = parseInt("0x" + hexString.substring(28, 30)) * -1;
snr = parseInt("0x" + hexString.substring(30, 32)) / 10;
// msg.timestamp = Date.now();
// var d = new Date();
// msg.timestring = d.toString();

// node.status({fill:"blue",shape:"dot",text:"Last Message recieved from: " + msg.nodeId + " @" + msg.timestring});



// return msg;

console.log(nodeId, orient, temp, pressure, humidity, movement, light, voltage, rssi, snr)
