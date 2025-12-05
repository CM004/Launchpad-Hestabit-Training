const mongoose = require('mongoose');
//const status = require('statuses');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    //match: [/^.+@.+\\..+$/, 'Please fill a valid email address']
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  password:{
    type: String,
    required:true,
    minlength: 8
  },
  status:{
    type: String,
    enum: ['active', 'inactive'],
    default: 'active'
  }
});

userSchema.pre('save', async function (next) {
    this.email = this.email.toLowerCase();

    this.password = await require('bcryptjs').hash(this.password, 10);

    // next();
});

userSchema.index({status: 1, createdAt: -1});

userSchema.set('toJSON', {
  transform: (doc,ret) => {   // Field transformation ( ret is the returned object)
    delete ret.password; // Remove the password field from the response
    ret.userId = ret._id; // Rename _id to userId for API consistency
    delete ret._id;
    delete ret.__v;
    return ret;
  }
});


module.exports = mongoose.model('User', userSchema);
