const express = require('express');
const router = express.Router();
const Food = require('../models/Meal');

router.get('/', async (req, res) => {
    try {
        let {
            minCalories, maxCalories, 
            minProtein, maxProtein, 
            minCarbs, maxCarbs, 
            minFat, maxFat
        } = req.query;

        let filter = {};

        if (minCalories) filter.calories = { ...filter.calories, $gte: parseFloat(minCalories) };
        if (maxCalories) filter.calories = { ...filter.calories, $lte: parseFloat(maxCalories) };

        if (minProtein) filter.proteins = { ...filter.proteins, $gte: parseFloat(minProtein) };
        if (maxProtein) filter.proteins = { ...filter.proteins, $lte: parseFloat(maxProtein) };

        if (minCarbs) filter.carbs = { ...filter.carbs, $gte: parseFloat(minCarbs) };
        if (maxCarbs) filter.carbs = { ...filter.carbs, $lte: parseFloat(maxCarbs) };

        if (minFat) filter.fats = { ...filter.fats, $gte: parseFloat(minFat) };
        if (maxFat) filter.fats = { ...filter.fats, $lte: parseFloat(maxFat) };

        const meals = await Food.aggregate([
            { $match: filter },   
            { $sample: { size: 3 } } 
        ]);
        
        res.json(meals);  
    } catch(err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
