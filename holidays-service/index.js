const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

mongoose.connect('mongodb://holidays-mongo:27017/holidaysdb', {
  useNewUrlParser: true, useUnifiedTopology: true
});

const HolidaySchema = new mongoose.Schema({
  name: String,
  location: String,
  price: Number
});

const Holiday = mongoose.model('Holiday', HolidaySchema);

app.get('/holidays', async (req, res) => {
  const holidays = await Holiday.find();
  res.json(holidays);
});

app.post('/holidays', async (req, res) => {
  const holiday = new Holiday(req.body);
  await holiday.save();
  res.json(holiday);
});

app.listen(5002, () => console.log('Holidays service running on port 5002'));