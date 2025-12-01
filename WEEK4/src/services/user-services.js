const User = require('../models/User');
const UserRepository = require('../repositories/user-repo');
const { NotFoundError, ValidationError } = require('../utils/errors');
const userRepository = new UserRepository(User);

async function createUser(userData) {
  const result = await userRepository.createUser(userData);
  return result; 
}

async function getAllUsers() {
  return await userRepository.findAllUsers();
}

async function getUserById(id) {
    const user = await userRepository.findUserById(id);
    if (!user){
        throw new NotFoundError("User not found");
    }
    return user 
}

async function getPaginatedUsers(page = 1, limit = 10) {
     return await userRepository.findPaginatedUsers(
      parseInt(page),
      parseInt(limit)
    );
}

async function updateUser(id, updateData) {
    const user = await userRepository.updateUser(id, updateData);
    if(!user){
        throw new NotFoundError("User not found")
    }
  return user;
}

async function deleteUser(id) {
    const user = await userRepository.deleteUser(id);
    if(!user){
        throw new NotFoundError("User Not found")
    }
  return user
}

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
  getPaginatedUsers
};