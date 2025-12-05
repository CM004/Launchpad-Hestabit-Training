const express = require('express');
const router = express.Router();
const productRoutes = require("./product.routes")
const userRoutes = require("./user.routes")

router.get('/', (req, res) => {
  res.json({message : "hi"});
});

router.use('/users', userRoutes);

router.use('/products', productRoutes);

module.exports = router;
