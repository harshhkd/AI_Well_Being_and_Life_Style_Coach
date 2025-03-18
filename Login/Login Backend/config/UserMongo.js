const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true }
});

const UserMongo = mongoose.model("User", UserSchema);

module.exports = UserMongo;
