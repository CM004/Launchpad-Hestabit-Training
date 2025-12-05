const winston = require('winston');
const path = require('path');

// Simple format - just the message
const simpleFormat = winston.format.printf(({ message, requestId }) => {
    const id = requestId ? `[${requestId}]` : '';
    return `${id} ${message}`;
});

// Format with timestamp for file
const fileFormat = winston.format.printf(({ message, requestId }) => {
  const timestamp = new Date().toString();
  const id = requestId ? `[${requestId}]` : '';
  return `${timestamp} ${id} - ${message}`;
});

// Create logger
const logger = winston.createLogger({
    format: winston.format.json(),
    transports: [
    // Console output (no timestamp)
    new winston.transports.Console({
      format: simpleFormat,
    }),
    // Single file output (with timestamp)
    new winston.transports.File({
      filename: path.join(__dirname, '../logs/app.log'),
      format: fileFormat,
    }),
  ],
});

module.exports = logger;
