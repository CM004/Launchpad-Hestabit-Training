const { v4: uuidv4 } = require('uuid');

function attachRequestId(req, res, next) {
  req.requestId = req.headers['x-request-id'] || uuidv4();
  res.setHeader('X-Request-ID', req.requestId);
  console.log(`Request ${req.requestId} received from client`);
  next();
}

module.exports = attachRequestId;
