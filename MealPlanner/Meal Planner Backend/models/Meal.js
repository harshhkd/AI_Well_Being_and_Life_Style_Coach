const mongoose = require('mongoose');

const MealSchema = new mongoose.Schema({
    description: String,
    calories: Number,
    proteins: Number,
    fats: Number,
    carbs: Number,
    cholestrol: Number,
    sugar: Number,
    calcium: Number,
    iron: Number,
    potassium: Number
});

module.exports = mongoose.model('Food', MealSchema, 'foods');