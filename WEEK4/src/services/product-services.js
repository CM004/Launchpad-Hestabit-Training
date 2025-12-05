const Product = require('../models/Product');
const ProductRepository = require('../repositories/product-repo');
const { NotFoundError, ValidationError } = require('../utils/errors');

const productRepoInstance = new ProductRepository(Product);

async function createProduct(productData) {
  if (!productData.name || productData.price === undefined) {
    throw new ValidationError("Name and price both are required");
  }
  return await productRepoInstance.createProduct(productData);
}

async function getAllProducts() {
  return await productRepoInstance.findAllProducts();
}

async function getProductById(id) {
  const product = await productRepoInstance.findProductById(id);
  if (!product || product.isDeleted) {
    throw new NotFoundError("Product not found");
  }
  return product;
}

async function getPaginatedProducts(page = 1, limit = 10) {
  return await productRepoInstance.findPaginatedProducts(page, limit);
}

async function updateProduct(id, updateData) {
  const product = await productRepoInstance.updateProduct(id, updateData);
  if (!product) {
    throw new NotFoundError("Product not found");
  }
  return product;
}

async function hardDeleteProduct(id) {
  const product = await productRepoInstance.deleteProduct(id);
  if (!product) {
    throw new NotFoundError("Product not found to delete");
  }
  return product;
}

async function softDeleteProduct(id) {
  const product = await productRepoInstance.softDeleteProduct(id);
  if (!product) {
    throw new NotFoundError("Product not found");
  }
  return product;
}

async function restoreDeletedProduct(id) {
  const restoredProduct = await productRepoInstance.restoreSoftDeletedProduct(id);
  if (!restoredProduct) {
    throw new NotFoundError("No such product deleted to restore");
  }
  return restoredProduct;
}

async function searchProducts(queryParams) {
  const {
    search,
    minPrice,
    maxPrice,
    tags,
    sort,
    page = 1,
    limit = 10,
    includeDeleted = "false"
  } = queryParams;

  // coerce numeric values
  const pageNum = Number(page) || 1;
  const limitNum = Number(limit) || 10;
  const skip = (pageNum - 1) * limitNum;

  const filter = {};

  if (includeDeleted !== "true") {
    filter.isDeleted = false;
  }

  if (search) {
    filter.$or = [
      { name: { $regex: search, $options: 'i' } },
      { description: { $regex: search, $options: 'i' } }
    ];
  }

  if (minPrice !== undefined || maxPrice !== undefined) {
    filter.price = {};
    if (minPrice !== undefined) filter.price.$gte = Number(minPrice);
    if (maxPrice !== undefined) filter.price.$lte = Number(maxPrice);
  }

  if (tags) {
    const tagArray = tags.split(',').map(t => t.trim()).filter(Boolean);
    if (tagArray.length) filter.tags = { $in: tagArray };
  }

  // build sort option (default newest first)
  let sortOption = { createdAt: -1 };
  if (sort) {
    const [field, order] = sort.split(':');
    if (field) {
      sortOption = { [field]: order === 'desc' ? -1 : 1 };
    }
  }

  // debug: uncomment to log filter during development
  // console.log('search filter:', JSON.stringify(filter), { sortOption, skip, limitNum });

  const products = await productRepoInstance.findProductsWithFilters(filter, {
    sort: sortOption,
    skip,
    limit: limitNum
  });

  const totalProductsWithFilters = await productRepoInstance.countProductsWithFilters(filter);

  return {
    products,
    pagination: {
      totalProductsWithFilters,
      page: pageNum,
      limit: limitNum,
      pages: Math.ceil(totalProductsWithFilters / limitNum)
    }
  };
}

module.exports = {
  searchProducts,
  getAllProducts,
  getProductById,
  createProduct,
  updateProduct,
  hardDeleteProduct,
  softDeleteProduct,
  restoreDeletedProduct,
  getPaginatedProducts
};
