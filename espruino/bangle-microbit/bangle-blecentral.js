// Status flags
var connected = false;
var txCharacteristic = false;

function bleConnect() {
  E.showMessage("Connecting...");
  NRF.requestDevice({ filters: [{ name: 'Espruino MICROBIT2' }] }).then(function(device) {
    return device.gatt.connect();
  }).then(function(d) {
    connected = d;
    return d.getPrimaryService("6e400001-b5a3-f393-e0a9-e50e24dcca9e");
  }).then(function(s) {
    return s.getCharacteristic("6e400002-b5a3-f393-e0a9-e50e24dcca9e");
  }).then(function(c) {
    txCharacteristic = c;
    E.showMessage("Connected to micro:bit :D");
  }).catch(function() {
    E.showMessage("Error Connecting");
    connected=false;
    if (connected) connected.disconnect();
  });
}

function sendCommand(cmd) {
  txCharacteristic.writeValue(cmd).catch(function() {
    E.showMessage("Error sending cmd");
    connected = false;
  });
}

setWatch(() => {
  Bangle.buzz();
  if (!connected) {
    bleConnect();
  } else {
    E.showMessage("Sending command to\nmicro:bit!");
    sendCommand('showFace()\n');
    setTimeout(() => g.clear(), 1000);
  }
}, BTN1, {repeat:true});

bleConnect();
