//‘use strict’;

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');


const hostname = '127.0.0.1';
const port = 3000;

// the web server to response a 'Hello world'


/*
const server = http.createServer((req,res) => {
    res.statusCode=200;
    res.setHeader('Content-type','text/html');
    res.end('<h1>Hello,world!</h1>');
});
server.listen(port,hostname,()=>{
    console.log(`Server is running at http://${hostname}:${port}/`);
});
*/


// a file server
var root = path.resolve(process.argv[2] || '.');
console.log('static root dir: ' + root);

const file_server = http.createServer(function(req,res) {
    console.log('Enter the server...');
    var pathname = url.parse(req.url).pathname;
    var filepath = path.join(root,pathname);
    fs.stat(filepath,(err,stat) => {
        if(!err && stat.isFile()){
            console.log('200 ' + req.url);
            res.statusCode = 200;
            fs.createReadStream(filepath).pipe(res);
        }else{
            console.log('404 ' + req.url);
            res.statusCode = 404;
            res.end('404 Not Found');
        }

    });
});


file_server.listen(port,hostname,() => {
    console.log(`File server is running at http://${hostname}:${port}/`);
});


