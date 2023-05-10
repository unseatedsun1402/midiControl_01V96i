const process = require('child_process').exec
process('test.py',function (stderr, stdout, ){
    console.log("Our Data: " + stdout)
})