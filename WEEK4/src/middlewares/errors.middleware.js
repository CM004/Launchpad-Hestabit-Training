function errorHandler(error, req, res, next) {
    const statusCode = error.statusCode || 500;
    const code = error.code || "INTERNAL_ERROR";
    res.status(statusCode).json({
        success:false,
        message:error.message || "Something went wrong",
        code : code,
        timestamp : error.timestamp || new Date().toString(),
        path : req.path
    });
}

module.exports = errorHandler;