const productService = require('../services/product-services');
const logger = require("../utils/logger");
async function searchProducts(req, res, next) {
  try {
    logger.info('Searching products', { requestId: req.requestId });
    const searchProductResult = await productService.searchProducts(req.query);
    res.json({
      success: true,
      data: searchProductResult
    });
  } catch (error) {
    next(error);
  }
}

async function getAllProducts(req, res, next){
    logger.info('Getting all products', { requestId: req.requestId });
    try{
        const allProducts = await productService.getAllProducts();
        res.json({
            success: true,
            data : allProducts
        });
    }
    catch (error){
        next(error)
    }
}

async function getProductById(req, res, next){
    logger.info('Getting product by id', { requestId: req.requestId });
    try{
        const product = await productService.getProductById(req.params.id);
        res.json({
            succes:true,
            data:product
        });
    }
    catch(error){
        next(error)
    }
}

async function createProduct(req, res, next){
    try{
        logger.info('Creating product', { requestId: req.requestId });
        const newProduct = await productService.createProduct(req.body);
        res.status(201).json({
            success:true,
            data:newProduct
        });
    }
    catch(error){
        next(error);
    }
}

async function getPaginatedProducts(req, res, next){
    logger.info('Getting paginated products', { requestId: req.requestId });
    try{
        const{page,limit} = req.query;
        const result = await productService.getPaginatedProducts(page,limit);
        res.json({
            success: true,
            data: result
        });
    }
    catch(error){
        next(error);
    }
}

async function updateProduct(req, res, next){
    logger.info('Updating product', { requestId: req.requestId });
    try{
        const updatedProduct = await productService.updateProduct(req.params.id, req.body);
        res.json({
            success:true,
            data: updatedProduct
        });
    }
    catch(error){
        next(error);
    }
}

//soft delete for user
async function deleteProduct(req, res, next){
    logger.info('Deleting product', { requestId: req.requestId });
    try{
        await productService.softDeleteProduct(req.params.id);
        res.json({
            success:true,
            message:"Product deleted successfully"
        });
    }
    catch(error){
        next(error);
    }
}

async function deleteProductAdmin(req, res, next){
    logger.info('Admin deleting product', { requestId: req.requestId });
    try{
        await productService.hardDeleteProduct(req.params.id);
        res.json({
            success: true,
            message: "Product deleted Permanently"
        });
    }
    catch(error){
        next(error);
    }
}

async function restoreProduct(req, res, next){
    logger.info('Restoring products', { requestId: req.requestId });
    try{
        const restoredProduct = await productService.restoreDeletedProduct(req.params.id);
        res.json ({
            success: true,
            message:"Product restored successfully",
            data: restoredProduct
        })
    }
    catch(error){
        next(error);
    }
}

module.exports = {
    createProduct,
    getAllProducts,
    getProductById,
    getPaginatedProducts,
    searchProducts,
    updateProduct,
    deleteProduct,
    deleteProductAdmin,
    restoreProduct
}
