const express = require('express');
const logger = require('../utils/logger');
const connectDatabase = require('./db');
const setupMiddlewares = require('../middlewares');
const routes = require('../routes');

async function loadApp() {
  const app = express();

  // Step 1: Setup middlewares
  setupMiddlewares(app);
  logger.info('Middlewares loaded');

  // Step 2: Connect database
  await connectDatabase();

  // Step 3: Add routes
  app.get('/health', function(req, res) {
    res.json({ status: 'OK' });
  });
  
  app.use('/users', routes);
  
  // 2 LINE SOLUTION - Count routes
  const allRoutes = app.router.stack.filter(r => r.route).length;
  const apiRoutes = routes.stack ? routes.stack.filter(r => r.route).length : 0;
  logger.info(`Routes mounted: ${allRoutes + apiRoutes} endpoints`);

  // Step 4: Handle errors
  app.use(function(error, req, res, next) {
    res.status(500).json({ error: error.message });
  });

  return app;
}

module.exports = loadApp;
