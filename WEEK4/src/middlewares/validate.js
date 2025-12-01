const Joi = require('joi');
const { ValidationError } = require('../utils/errors');

//Product
const productSchemas = {
  create: Joi.object({
    name: Joi.string().min(3).required(),
    price: Joi.number().min(0).required(),
    ratings : Joi.array().items(Joi.number().min(1).max(5)).optional(),
    description: Joi.string().max(500).optional(),
    tags: Joi.array().items(Joi.string()).optional(),
    status: Joi.string().valid('available', 'unavailable').optional()
  }),

  update: Joi.object({
    name: Joi.string().min(3).optional(),
    price: Joi.number().min(0).optional(),
    ratings: Joi.array().items(Joi.number().min(1).max(5)).optional(),
    description: Joi.string().max(500).optional(),
    tags: Joi.array().items(Joi.string()).optional(),
    status: Joi.string().valid('available', 'unavailable').optional()
  }).min(1),

  search: Joi.object({
    search: Joi.string().max(100).optional(),
    minPrice: Joi.number().min(0).optional(),
    maxPrice: Joi.number().min(0).optional(),
    tags: Joi.string().optional(),
    sort: Joi.string().pattern(/^[a-zA-Z]+:(asc|desc)$/).optional(),
    page: Joi.number().integer().min(1).optional(),
    limit: Joi.number().integer().min(1).max(100).optional(),
    includeDeleted: Joi.string().valid('true', 'false').optional()
  })
};

// User schemas
const userSchemas = {
  create: Joi.object({
    name: Joi.string().min(3).required(),
    email: Joi.string().lowercase().email().required(),
    password: Joi.string().min(8).pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/).required(),
    status: Joi.string().valid('active', 'inactive').optional()
  }),

  update: Joi.object({
    name: Joi.string().min(3).optional(),
    email: Joi.string().email().lowercase().optional(),
    password: Joi.string().min(8).pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/).optional(),
    status : Joi.string().valid('active', 'inactive').optional()
  }).min(1),

  search: Joi.object({
    name: Joi.string().min(3).optional(),
    email: Joi.string().email().lowercase().optional(),
    status: Joi.string().valid('active','inactive').optional()
  })
};

// Validation middleware
function validate(type, entity = 'product') {
  return (req, res, next) => {
    const schemas = entity === 'user' ? userSchemas : productSchemas;
    const dataToValidate = type === 'search' ? req.query : req.body;
    const { error } = schemas[type].validate(dataToValidate);
    if (error) {
      throw new ValidationError(error.details[0].message);
    }
    next();
  };
}

module.exports = validate;
