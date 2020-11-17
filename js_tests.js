
let data = 'AAB296C4E5094228BA0000EC0000009A2D64'

let output = {
    id: data.substring(0, 8),
    temp: parseInt(data.substring(10, 12) + data.substring(8, 10), 16) / 100,
    pressure: parseInt(data.substring(14, 16) + data.substring(12, 14), 16) / 10,
    humidity: parseInt(data.substring(16, 18), 16) % 128,
    voltage: parseInt(data.substring(22, 24), 16) / 50,
    rssi: parseInt(data.substring(data.length - 4, data.length - 2), 16) * -1,
    snr: parseInt(data.substring(data.length - 2, data.length), 16) / 10,
};

console.log(output)


let sensorType = 'droplet'
let nodeID = 'AAB296C4'.toUpperCase() || '';
if (!data) return;
if (data.length % 2 === 1 && (data[data.length - 1] === '\r' || data[data.length - 1] === '\n')) {
    data = data.substring(0, data.length - 1);
} else if (data.substring(data.length - 2, data.length) === '\r\n') {
    data = data.substring(0, data.length - 2);
}
console.log(111)
if (data.length !== 36 && data.length !== 44 && data.substring(2, 4) !== 'AA' && data.substring(2, 4) !== 'B0' && data.substring(2, 4) !== 'B1' && data.substring(2, 4) !== 'B2') return;
console.log(2222)

if (nodeID == data.substring(0, 8) || nodeID == '') {
    console.log(3333)
    if (sensorType === 'microedge' && data.substring(2, 4) === 'AA' && (data.length === 44 || data.length === 36)) {
        console.log('microedge')
        
        // if (this.inputs[0].updated) this.resetWatchdog();
        // this.writeOutputs(this.microEdgeDecode(data));
    } else if ( sensorType === 'droplet' && data.substring(2, 3) === 'B' && (data.length === 44 || data.length === 36)) {
        console.log('droplet')
        // if (this.inputs[0].updated) this.resetWatchdog();
        // this.writeOutputs(this.dropletDecode(data));
    }
}


