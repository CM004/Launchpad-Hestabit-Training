const express = require('express');
const os = require('os');
const app = express();

app.get('/api', (req, res) => {
  res.json({ 
    message: 'Secure API Response', 
    protocol: req.headers['x-forwarded-proto'] || req.protocol,
    container: os.hostname()
  });
});

app.listen(3000, () => console.log('Backend running on 3000'));
