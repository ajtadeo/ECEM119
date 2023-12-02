const express = require('express');
const app = express();
const host = '172.20.10.2'; // ipconfig getifaddr en0
const port = 9000;

app.use(express.json());

app.post('/api/data', (req, res) => {
  console.log(req.body);
  res.send(req.body);
});

app.listen(port, host, () => {
  console.log(`Server is listening on ${host}:${port}`);
});