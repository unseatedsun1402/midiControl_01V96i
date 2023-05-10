
//const process = require('child_process');
const express = require('express');
const server = express();
const progPath = __dirname + '/midiControl_01V96I.py';

// Creates a server which runs on port 3000 and 
// can be accessed through localhost:3000
server.listen(3000, function() {
  console.log('server running on port 3000');
} )

// Function callName() is executed whenever 
// url is of the form localhost:3000/name
server.get('/req', callReq);

function callReq(req, res) {
    
  // Use child_process.spawn method from 
  // child_process module and assign it
  // to variable spawn
  var spawn = require("child_process").spawn;
    
  // Parameters passed in spawn -
  // 1. type_of_script
  // 2. list containing Path of the script
  //    and arguments for the script 
    
  // E.g : http://localhost:3000/name?firstname=Mike&lastname=Will
  // so, first name = Mike and last name = Will
  var process = spawn('python3',[progPath] );

  // Takes stdout data from script which executed
  // with arguments and send this data to res object
  process.stdout.on('data', function(data) {
      res.send(data.toString());
  } )
}