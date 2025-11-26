const User = require('../models/User');
const UserRepository = require('../repositories/user-repo');

const userRepository = new UserRepository(User);

async function createUser(userData) {
  return await userRepository.createUser(userData);
}

async function getAllUsers() {
  return await userRepository.findAllUsers();
}

async function getUserById(id) {
  return await userRepository.findUserById(id);
}

async function getPaginatedUsers(page, limit) {
  return await userRepository.findPaginatedUsers(page, limit);
}

async function updateUser(id, updateData) {
  return await userRepository.updateUser(id, updateData);
}

async function deleteUser(id) {
  return await userRepository.deleteUser(id);
}

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
  getPaginatedUsers
};