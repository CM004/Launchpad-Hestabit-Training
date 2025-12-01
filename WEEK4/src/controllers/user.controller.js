const userService = require('../services/user-services');

class UserController {
  async createUser(req, res, next) {
  try {
    const newUser = await userService.createUser(req.body);
    res.status(201).json({ success: true, data: newUser });
  } catch (error) {
    next(error);
  }}


  async getAllUsers(req, res, next) {
    try {
      const result = await userService.getAllUsers(req.query);
      res.json({ success: true, data: result });
    } catch (error) {
      next(error);
    }
  }

  async getPaginatedUsers(req,res,next){
    try{
        const {page,limit} = req.query;
        const users = await userService.getPaginatedUsers(page,limit);
        res.json({success: true, data: users});
    }catch(error){
        next(error);
    }
  }

  async getUserById(req, res, next) {
    try {
      const user = await userService.getUserById(req.params.id);
      res.json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  }

  async updateUser(req, res, next) {
    try {
      const user = await userService.updateUser(req.params.id, req.body);
      res.json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  }

  async deleteUser(req, res, next) {
    try {
      const user = await userService.deleteUser(req.params.id);
      res.json({ success: true, message: 'User deleted', data: user });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new UserController();
