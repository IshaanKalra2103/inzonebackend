const functions = require('firebase-functions');
const { execFile } = require('child_process');
const path = require('path');

exports.api = functions.https.onRequest((req, res) => {
    const scriptPath = path.join(__dirname, 'main.py');
    execFile('python', [scriptPath], (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            res.status(500).send(error);
            return;
        }
        res.send(stdout);
    });
});
