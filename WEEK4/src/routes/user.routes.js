const express = require('express');
const router = express.Router();
const User = require('../models/User');
const userController = require("../controllers/user.controller");
const { validate } = require('../middlewares');
const { apiLimiter } = require('../middlewares/security');

// routes
router.get('/', userController.getAllUsers);
router.get('/paginated',userController.getPaginatedUsers);
router.get('/:id', userController.getUserById);
router.post('/', apiLimiter, validate('create', 'user'), userController.createUser);
router.put('/:id', validate('update', 'user'), userController.updateUser);
router.delete('/:id', userController.deleteUser);

module.exports = router;
