const {shell} = require('electron');
var path = require('path');
var sys = require('sys');
var exec = require('child_process').exec;
var child = null;

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
    });

    child.on('exit', function() {
        child = null;
    });
}

function launchPython(evt) {
    var nodeConsole = require('console');
    var myConsole = new nodeConsole.Console(process.stdout, process.stderr);

    var command = evt.srcElement.id;

    spawnChildIfNeeded();

    if (command == "sendData") {
        myConsole.log('\x1b[34m%s\x1b[0m','PRINT BEFORE PYTHON EXEC FROM NODE.JS');

        child.stdin.write("sendData\n");
        //this is a listener for peers output
        myConsole.log('\x1b[36m%s\x1b[0m','PIPED FROM PYTHON PROGRAM: ' + data.toString());

    }else if(command == "sendSMS"){
        myConsole.log('\x1b[34m%s\x1b[0m','INTERACTION IN JS');

        child.stdin.write("sendSMS\n+123456");
        //this is a listener for peers output
        myConsole.log('\x1b[36m%s\x1b[0m','PIPED FROM PYTHON PROGRAM: ' + data.toString());

    }else if(command == "sendSensor"){
        myConsole.log('\x1b[34m%s\x1b[0m','EXIT IN JS');

        child.stdin.write("sendSensor\n");
        //this is a listener for peers output
        myConsole.log('\x1b[36m%s\x1b[0m','PIPED FROM PYTHON PROGRAM: ' + data.toString());

        //child.stdin.end();

        // var nodeConsole = require('console');
        // var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
        // myConsole.log('python terminated from js too');
    }

}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("sendData").addEventListener("click", launchPython);
  document.getElementById("sendSMS").addEventListener("click", launchPython);
  document.getElementById("sendSensor").addEventListener("click", launchPython);
})
