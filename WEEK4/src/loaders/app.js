const express = require('express');
const logger = require('../utils/logger');
const connectDatabase = require('./db');
const routes = require('../routes');
const errorHandler = require("../middlewares/errors.middleware");
const {setupMiddlewares} = require('../middlewares/index');

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
  
  app.use('/', routes);

  const allRoutes = app.router.stack.filter(r => r.route).length;
  const apiRoutes = routes.stack ? routes.stack.filter(r => r.route).length : 0;
  logger.info(`Routes mounted: ${allRoutes + apiRoutes} endpoints`);

  app.use(errorHandler);

  return app;
}

module.exports = loadApp;
