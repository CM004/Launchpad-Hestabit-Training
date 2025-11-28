const express = require('express');
const router = express.Router();
const Product = require('../models/Product');
const productController = require("../controllers/product.controller");

// Search with filters (must be before /:id)
router.get('/search', productController.searchProducts);

// Paginated products
router.get('/paginated', productController.getPaginatedProducts);

// Get all products
router.get('/', productController.getAllProducts);

// Get single product
router.get('/:id', productController.getProductById);

// Create product
router.post('/', productController.createProduct);

// Update product
router.put('/:id', productController.updateProduct);

// Soft delete (for users)
router.delete('/:id', productController.deleteProduct);

// Hard delete (for admin only)
router.delete('/:id/permanent', productController.deleteProductAdmin);

// Restore soft deleted product
router.post('/:id/restore', productController.restoreProduct);

module.exports = router;    