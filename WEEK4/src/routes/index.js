const express = require('express');
const router = express.Router();

// Example routes

router.get('/', (req, res) => {
  res.send("hi")
});
router.get('/users', (req, res) => {
  res.json({ message: 'Get all users' });
});

router.post('/users', (req, res) => {
  res.json({ message: 'Create user' });
});

router.get('/products', (req, res) => {
  res.json({ message: 'Get all products' });
});

router.get('/products', (req, res) => {
  res.json({ message: `Create product ` });
});

module.exports = router;
