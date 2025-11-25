const loadApp = require('./loaders/app');
const logger = require('./utils/logger');
const config = require('./config');

async function startServer() {
  try {
    // Load the app (this logs: Middlewares, Database, Routes)
    const app = await loadApp();
    
    // Start server (this logs: Server started)
    const serverPort = config.port;
    app.listen(serverPort, () => {
      logger.info(`Server started on port ${serverPort}`);
    });
    
  } catch (error) {
    logger.error('Server failed: ' + error.message);
  }
}

startServer();
