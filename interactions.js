const {shell} = require('electron');
var path = require('path');
var sys = require('sys');
var exec = require('child_process').exec;
var child = null;
var curStatusBox = null;

function spawnChildIfNeeded() {
    if(child != null) {
        return;
    }
    var nodeConsole = require('console');
    var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
    myConsole.log('Launching Python');
    
    // EXECUTION OF PYTHON
    child = exec("python -u hologram-python.py", function (error, stdout, stderr) {
      if (error !== null) {
        console.log('exec error: ' + error);
      }
    });

    //this is a listener for peers output
    child.stdout.on('data', function(data) {
      var nodeConsole = require('console');
      var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
      myConsole.log('\x1b[36m%s\x1b[0m', 'PIPED FROM PYTHON PROGRAM: ' + data.toString());
      if(data.startsWith("Done")) {
          curStatusBox.innerText = "Done";
      } else if(data.startsWith("Got SMS:")) {
          sms = data.substr(8);
          document.getElementById('sms-recv-box').innerText = sms;
      }
    });

    child.on('exit', function() {
        child = null;
        curStatusBox.innerText = "Done";
    });
}

function launchPython(evt) {
    if (evt.preventDefault) evt.preventDefault();

    var nodeConsole = require('console');
    var myConsole = new nodeConsole.Console(process.stdout, process.stderr);

    var command = evt.srcElement.id;

    spawnChildIfNeeded();

    if (command == "sendData") {
        myConsole.log('\x1b[34m%s\x1b[0m','PRINT BEFORE PYTHON EXEC FROM NODE.JS');

        curStatusBox = document.getElementById('sendDataStatus');

        child.stdin.write("sendData\n");
    } else if(command == "send-sms-form"){
        myConsole.log('\x1b[34m%s\x1b[0m','INTERACTION IN JS');

        curStatusBox = document.getElementById('sendSMSStatus');
        phone = document.getElementById('phone').value;

        myConsole.log('\x1b[34m%s\x1b[0m',phone);

        child.stdin.write("sendSMS\n"+phone+"\n");
    } else if(command == "sendSensor"){
        myConsole.log('\x1b[34m%s\x1b[0m','EXIT IN JS');

        curStatusBox = document.getElementById('sendSensorStatus');

        child.stdin.write("sendSensor\n");
    }

    curStatusBox.innerText = "Running...";

    return false;
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("sendData").addEventListener("click", launchPython);
  document.getElementById("send-sms-form").addEventListener("submit", launchPython);
  document.getElementById("sendSensor").addEventListener("click", launchPython);
})
