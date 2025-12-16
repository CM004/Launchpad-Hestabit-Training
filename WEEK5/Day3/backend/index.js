const express = require('express');
const os = require('os');

const app = express();
const PORT = 3000;
const hostname = os.hostname();

app.get("/api", (req, res) => {
  res.json({ message: "Server is running", dockerContainer: hostname });
});

app.listen(PORT, () => console.log(`Backend running on ${PORT} - ${hostname}`));
