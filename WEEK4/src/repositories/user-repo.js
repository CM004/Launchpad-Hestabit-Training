class UserRepository {
  constructor(UserModel) {
    this.UserModel = UserModel;
  }

  async createUser(userData) {
    const newUser = new this.UserModel(userData);
    return await newUser.save();
  }

  async findAllUsers() {
    return await this.UserModel.find({});
  }

  async findUserById(id) {
    return await this.UserModel.findById(id);
  }

  async findPaginatedUsers(page = 1, limit = 10) {
    const skip = (page - 1) * limit;
    const users = await this.UserModel.find().skip(skip).limit(limit);
    const total = await this.UserModel.countDocuments();
    return {
      users,
      total,
      page,
      pages: Math.ceil(total / limit)
    };
  }

  async updateUser(id, updateData) {
    delete updateData.password; // Prevent password updates through this method
    return await this.UserModel.findByIdAndUpdate(id, updateData, { new: true });
  }

  async deleteUser(id) {
    return await this.UserModel.findByIdAndDelete(id);
  } 
}

module.exports = UserRepository;
