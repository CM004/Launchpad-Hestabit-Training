const productService = require('../services/product-services');

async function searchProducts(req, res, next) {
  console.log('REQ.QUERY ->', req.query);
  try {
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
