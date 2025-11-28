const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    price: {
        type: Number,
        required: true,
    },
    description: {
        type: String,
        unique: true
    },
    ratings: [{
            type: Number, // Individual rating from 1 to 5
            min: 1,
            max: 5
        }],
    createdAt: {
        type: Date,
        default: Date.now,
    },
    status:{
        type: String,
        enum: ['available', 'unavailable'],
        default: 'available'
    },
    //soft delete fields
    isDeleted: {
        type: Boolean,
        default: false
    },
    deletedAt: {
        type: Date,
        default: null
    },
    tags:[{
        type: String
    }]
});

productSchema.index({status: 1, createdAt: -1});

productSchema.virtual('fullName').get(function() {
  return `${this.name} ${this.price}`;
});

productSchema.virtual('computedRating').get(function() {
        if (this.ratings && this.ratings.length > 0) {
            const totalRating = this.ratings.reduce((acc, rating) => acc + rating, 0);
            return totalRating / this.ratings.length;
        }
        return 0; // Default to 0 if no ratings exist
});

productSchema.set('toJSON', { virtuals: true });
productSchema.set('toObject', { virtuals: true });

module.exports = mongoose.model('Product', productSchema);