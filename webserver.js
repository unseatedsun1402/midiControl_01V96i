const http = require('http');
const fs = require('fs').promises;
//const { isBuffer } = require('util');
const host = 'localhost';
const port = 8000;
const {spawn} = require('child_process');

const ver = spawn('python',['--version.py']);
ver.stdout.on('data', (data)=>{
    console.log('stdout: ${data}')
});
ver.stderr.on('data',(data)=>{
    console.error('stderr: ${data}')
});

let indexFile;

const requestListener = function (req, res) {
    res.setHeader("Content-Type", "text/html");
    res.writeHead(200);
    res.end(indexFile);
};

const server = http.createServer(requestListener);

fs.readFile(__dirname + "/index.html")
    .then(contents => {
        indexFile = contents;
        server.listen(port, host, () => {
            console.log(`Server is running on http://${host}:${port}`);
        });
    })
    .catch(err => {
        res.writeHead(400)
        console.error(`Could not read index.html file: ${err}`);
        process.exit(1);
    });