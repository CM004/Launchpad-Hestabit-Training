const {setupSecurity} = require("./security");
const validate = require("./validate");

// Function to setup all middlewares
function setupMiddlewares(app) {
  setupSecurity(app)
}

// Export
module.exports = {setupMiddlewares, validate}
