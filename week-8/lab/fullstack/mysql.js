const express = require('express');
const multer = require('multer');
const mysql = require('mysql2');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static('uploads'));

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '1234', // Password
  database: 'gallery'
});

const storage = multer.diskStorage({
  destination: './uploads/',
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});
const upload = multer({ storage });

app.post('/upload', upload.single('image'), (req, res) => {
  const photo = req.file.filename;
  db.query(
    'INSERT INTO images (photo) VALUES (?)',
    [photo],
    (err, result) => {
      if (err) return res.status(500).send(err);
      res.json({ id: result.insertId, photo });
    }
  );
});

app.get('/images', (req, res) => {
  db.query('SELECT * FROM images ORDER BY created_at DESC', (err, results) => {
    if (err) return res.status(500).send(err);
    res.json(results);
  });
});

app.listen(8800, () => console.log('Server running on port 8800'));
