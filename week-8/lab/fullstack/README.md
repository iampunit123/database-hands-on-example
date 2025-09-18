# 📸 Gallery App

A simple gallery project using **Node.js**, **React**, and **MySQL**. It shows you how users can store and display images directly from a MySQL database 💾✨

---

## 🛠️ Tech Stack

**Frontend:** React + TailwindCSS 🎨  
**Backend:** Node.js + Express 🚀  
**Database:** MySQL 🐬

---

## 🏃‍♂️ Run It Locally

### 1️⃣ Create a Database

```sql
CREATE DATABASE gallery;
```

### 2️⃣ Create a Table

```sql
CREATE TABLE images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  photo VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3️⃣ Clone the Project

```bash
git clone https://github.com/PLP-Database-DEPT/gallery.git
```

### 4️⃣ Go to the Project Folder

```bash
cd lab-7
```

### 5️⃣ Install Dependencies

```bash
npm install
```

### 6️⃣ Start the Server

```bash
npm start 
```
### 7️⃣ Start the Frontend (in a new terminal)
```bash
cd client
npm run dev
```
---
