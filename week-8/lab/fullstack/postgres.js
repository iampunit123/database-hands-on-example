const { Pool } = require('pg');
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static('uploads'));

const db = new Pool({
  host: 'localhost',
  user: 'postgres',
  password: '1234',
  database: 'week8',
  port: 5432
});

const storage = multer.diskStorage({
  destination: './uploads/',
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage });

app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    const photo = req.file.filename;
    const result = await db.query(
      'INSERT INTO images (photo) VALUES ($1) RETURNING id',
      [photo]
    );
    res.json({ id: result.rows[0].id, photo });
  } catch (err) {
    res.status(500).send(err);
  }
});

app.get('/images', async (req, res) => {
  try {
    const results = await db.query('SELECT * FROM images ORDER BY created_at DESC');
    res.json(results.rows);
  } catch (err) {
    res.status(500).send(err);
  }
});

app.listen(8800, () => console.log('Server running on port 8800'));
