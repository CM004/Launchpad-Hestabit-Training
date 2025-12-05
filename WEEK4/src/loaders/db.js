const mongoose = require('mongoose');
const logger = require('../utils/logger');

async function connectDatabase() {
  try {
    const databaseUrl = process.env.MONGODB_URI;
    
    await mongoose.connect(databaseUrl);
    
    logger.info('Database connected');
    
  } catch (error) {
    logger.error('Database failed: ' + error.message);
    process.exit(1);
  }
}

module.exports = connectDatabase;
