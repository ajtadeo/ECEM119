// Chart data
var times = []
var acc = {
  x: [],
  y: [],
  z: []
}
var gyro = {
  x: [],
  y: [],
  z: []
}

// Server
const express = require('express');
const app = express();
const host = '172.20.10.2'; // ipconfig getifaddr en0
const port = 9000;

app.use(express.json());
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/static'));

app.get('/', (req, res) => {
  res.render('index', {
    acc: acc,
    gyro: gyro,
    times: times
  })
})

app.post('/api/data', (req, res) => {
  // update data
  var data = req.body["data"].split(" ");
  console.log(data)
  acc.x.push(parseFloat(data[0]));
  acc.y.push(parseFloat(data[1]));
  acc.z.push(parseFloat(data[2]));
  gyro.x.push(parseFloat(data[3]));
  gyro.y.push(parseFloat(data[4]));
  gyro.z.push(parseFloat(data[5]));
  times.push(parseInt(data[6]));

  res.sendStatus(200);
});

app.listen(port, host, () => {
  console.log(`Server is listening on ${host}:${port}`);
});