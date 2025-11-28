const express = require('express');
const logger = require('../utils/logger');
const connectDatabase = require('./db');
const setupMiddlewares = require('../middlewares');
const routes = require('../routes');
const error = require ("../utils/errors")

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
//   const totalEndpoints = app.router?.stack?.length;
//   logger.info(`Routes mounted: ${totalEndpoints} endpoints`);

  // Step 4: Handle errors
  app.use(function(error, req, res, next) {
    const statusCode = error.statusCode || 500;
    const code = error.code || "INTERNAL_ERROR";
    res.status(statusCode).json({
        success:false,
        message:error.message || "Something went wrong",
        code : code,
        timestamp : error.timestamp || new Date().toString(),
        path : req.path
    });
 });

  return app;
}

module.exports = loadApp;
