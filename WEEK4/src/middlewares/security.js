const rateLimit = require('express-rate-limit');
//const mongoSanitize = require('express-mongo-sanitize');
const helmet = require('helmet');
const cors = require('cors');
const express = require('express');

// Rate limiters
const apiLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 15, // 15 requests
  message: { success: false, message: 'Too many requests' }
});

// Setup function
function setupSecurity(app) {
  app.use(helmet()); // Security headers
  //app.use(mongoSanitize()); // Remove $ and . from input
  app.use(express.json({ limit: '10kb' }));
  if (process.env.NODE_ENV === 'production') {
    app.use(cors({ origin: "my-fd-url", credentials: true }));
  } else {
    app.use(cors()); // Allow all
  }
}

module.exports = { setupSecurity, apiLimiter};
