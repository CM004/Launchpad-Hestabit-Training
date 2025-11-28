// Import middleware packages
const cors = require('cors');
const helmet = require('helmet');
const express = require('express');

// Function to setup all middlewares
function setupMiddlewares(app) {
  app.use(helmet());           // Security headers
  app.use(cors());             // Allow browser requests
  app.use(express.json());     // Parse JSON data
}

// Export the function
module.exports = setupMiddlewares;
