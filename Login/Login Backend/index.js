const express = require('express');
const cors = require('cors');
const connectMongoDB = require('./config/mongodb.js');

const app = express();
app.use(express.json());
app.use(cors());

connectMongoDB();

const authRoutes = require('./routes/authRoutes');
app.use('/auth', authRoutes);

app.listen(8181, () => console.log("Server running on port 8181"));