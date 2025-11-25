const winston = require('winston');
const path = require('path');

// Simple format - just the message
const simpleFormat = winston.format.printf(({ message }) => {
  return message;
});

// Format with timestamp for file
const fileFormat = winston.format.printf(({ message }) => {
  const timestamp = new Date().toString();
  return `${timestamp} - ${message}`;
});

// Create logger
const logger = winston.createLogger({
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
