
const express = require('express');
const app = express();
const port = 3010;
const csv_file = require(__dirname + '/utils/data').parser;
const path = require('path');
const cors = require('cors');
const { parser } = require('./utils/data');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());
let index;

app.get('/', function (req, res) {
    res.send('GET request to the homepage');
});

app.get('/data', (req, res) => {
    console.log(csv_file[index]);
    return res.send(csv_file[index]);
})

app.get('/alert_list', () => {

});

app.get('/*', (req, res) => {
    res.send("404");
});

app.listen(port, () => { console.log("Starting server adsum on port:" + port) });
index = parser.length - 501;
console.log(index);
setInterval(() => {
    index--;
}, 1000);