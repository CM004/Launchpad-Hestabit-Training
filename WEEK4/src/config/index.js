const dotenv = require('dotenv');
const path = require('path');

// Load environment file based on NODE_ENV
function loadEnvironmentFile() {
  const environment = process.env.NODE_ENV || 'local';
  
  let environmentFileName;
  
  if (environment === 'production') {
    environmentFileName = '.env.prod';
  } else if (environment === 'development') {
    environmentFileName = '.env.dev';
  } else {
    environmentFileName = '.env.local';
  }
  
  const environmentFilePath = path.join(process.cwd(), environmentFileName);
  dotenv.config({ path: environmentFilePath });
  
  console.log(`Loaded environment config: ${environmentFileName}`);
}

loadEnvironmentFile();

// Export config values
const config = {
  port: process.env.PORT || 3000,
  mongoUri: process.env.MONGODB_URI,
  environment: process.env.NODE_ENV || 'local',
};

module.exports = config;
