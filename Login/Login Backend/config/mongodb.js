const mongoose = require('mongoose');

const connectMongoDB = async () => {
    try {
        await mongoose.connect("mongodb://localhost:27017/authDB", {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        console.log("Connected to MongoDB");
    } catch(error) {
        console.error("MongoDB Connection Error: ", error);
    }
}

module.exports = connectMongoDB;