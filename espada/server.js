const express = require("express");
const bodyParser = require("body-parser");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");

const app = express();
const db = new sqlite3.Database("users.db");

app.use(cors());
app.use(bodyParser.json());

// Create table if not exists
db.run(`CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  age INTEGER,
  gender TEXT,
  email TEXT UNIQUE,
  password TEXT,
  photo TEXT
)`);

// Signup route
app.post("/signup", (req, res) => {
  const { name, age, gender, email, password } = req.body;

  db.run(
    `INSERT INTO users (name, age, gender, email, password) VALUES (?, ?, ?, ?, ?)`,
    [name, age, gender, email, password],
    function (err) {
      if (err) return res.status(400).json({ error: "Email already exists!" });
      res.json({ message: "User registered successfully!" });
    }
  );
});

// Login route
app.post("/login", (req, res) => {
  const { email, password } = req.body;

  db.get(
    `SELECT * FROM users WHERE email = ? AND password = ?`,
    [email, password],
    (err, row) => {
      if (err) return res.status(500).json({ error: err.message });
      if (!row) return res.status(400).json({ error: "Invalid credentials" });

      res.json({ success: true, email: row.email });
    }
  );
});

// Profile route
app.get("/profile/:email", (req, res) => {
  const email = req.params.email;
  db.get(`SELECT * FROM users WHERE email = ?`, [email], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(row || {});
  });
});

// Upload photo route
app.post("/upload-photo", (req, res) => {
  const { email, photo } = req.body;
  db.run(
    `UPDATE users SET photo = ? WHERE email = ?`,
    [photo, email],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ message: "Photo updated!" });
    }
  );
});

app.listen(3000, () => console.log("Server running on http://localhost:3000"));
