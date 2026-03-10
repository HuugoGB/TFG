function errorHandler(err, req, res, next) {
    console.error(err); // Log para debug
    res.status(err.status || 500).json({
        error: true,
        message: err.message || "Error interno del servidor"
    });
}

module.exports = {errorHandler};