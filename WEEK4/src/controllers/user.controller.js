const userService = require('../services/user-services');
const logger = require("../utils/logger");
const {sendWelcomeEmail} = require("../jobs/email.job")

class UserController {
  async createUser(req, res, next) {
  try {
    logger.info('Creating user', { requestId: req.requestId });
    const newUser = await userService.createUser(req.body);

    sendWelcomeEmail(newUser, req.requestId).catch(err => 
        logger.error('Email queue failed', { requestId: req.requestId })
      );

    res.status(201).json({ success: true, data: newUser });
  } catch (error) {
    next(error);
  }}


  async getAllUsers(req, res, next) {
    try {
      logger.info('Getting all users', { requestId: req.requestId });
      const result = await userService.getAllUsers(req.query);
      res.json({ success: true, data: result });
    } catch (error) {
      next(error);
    }
  }

  async getPaginatedUsers(req,res,next){
    try{
        logger.info('Getting all paginated users', { requestId: req.requestId });
        const {page,limit} = req.query;
        const users = await userService.getPaginatedUsers(page,limit);
        res.json({success: true, data: users});
    }catch(error){
        next(error);
    }
  }

  async getUserById(req, res, next) {
    try {
      logger.info('Getting user by id', { requestId: req.requestId });
      const user = await userService.getUserById(req.params.id);
      res.json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  }

  async updateUser(req, res, next) {
    try {
      logger.info('Updating user', { requestId: req.requestId });
      const user = await userService.updateUser(req.params.id, req.body);
      res.json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  }

  async deleteUser(req, res, next) {
    try {
      logger.info('Deleting user', { requestId: req.requestId });
      const user = await userService.deleteUser(req.params.id);
      res.json({ success: true, message: 'User deleted', data: user });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new UserController();
