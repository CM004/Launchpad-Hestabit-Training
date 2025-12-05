const {setupSecurity} = require("./security");
const validate = require("./validate");
const attachRequestId = require("../utils/tracing");

// Function to setup all middlewares
function setupMiddlewares(app) {
    app.use(attachRequestId);
    setupSecurity(app);
}

// Export
module.exports = {setupMiddlewares, validate}
