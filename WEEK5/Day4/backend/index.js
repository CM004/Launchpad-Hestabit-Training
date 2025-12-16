const express = require('express');
const os = require('os');
const app = express();

app.get('/', (req, res) => {
  res.json({ 
    message: 'Secure API Response', 
    protocol: req.protocol,
    container: os.hostname()
  });
});

app.listen(3000, () => console.log('Backend running on 3000'));
