## 🎯 Hands-on Class Activity
_Your mission today as a junior database administrator is to explore how employees, projects, and addresses are connected._

You’ll use different types of **JOINs** to uncover hidden stories inside the database.
### 🚀 Joins and Relationships
#### 📚 Relationships in MySQL
In databases, relationships describe how tables are connected.
##### 1️⃣ One-to-One
One row in Table A is linked to exactly one row in Table B.
```sql
USE salesdb;
-- Staff table
CREATE TABLE staff (
  staffId INT PRIMARY KEY,
  FullName VARCHAR(100) NOT NULL
);

-- IDCard table (1:1 with Staff)
CREATE TABLE IDCard (
  CardId INT PRIMARY KEY,
  staffId INT UNIQUE, -- ensures only one card per employee
  IssueDate DATE,
  FOREIGN KEY (staffId) REFERENCES staff(staffId)
);

-- Insert sample data
INSERT INTO staff VALUES (1, 'Brian Otieno'), (2, 'Faith Wanjiru');
INSERT INTO IDCard VALUES (101, 1, '2025-01-01'), (102, 2, '2025-01-10');

-- Join to see the relationship
SELECT S.FullName, C.CardId, C.IssueDate
FROM staff S
INNER JOIN IDCard C ON S.EmployeeId = C.staffId;

```
#### 🏗️ Database Setup
We’ve created a simple system with employees, their projects, and where they live.
```sql
CREATE DATABASE safari;
USE safari;

-- Employees table
CREATE TABLE Employee (
  EmployeeId INT PRIMARY KEY,
  FullName VARCHAR(45) NOT NULL,
  Department VARCHAR(45) NOT NULL,
  Salary DECIMAL(10,2) NOT NULL,
  Gender VARCHAR(45) NOT NULL,
  Age INT NOT NULL
);

INSERT INTO Employee (EmployeeId, FullName, Department, Salary, Gender, Age) VALUES 
(1001, 'Brian Otieno', 'IT', 65000, 'Male', 25),
(1002, 'Faith Wanjiru', 'HR', 75000, 'Female', 27),
(1003, 'Peter Mwangi', 'Finance', 80000, 'Male', 28),
(1004, 'Michael Oduor', 'Finance', 82000, 'Male', 29),
(1005, 'Lilian Njeri', 'HR', 90000, 'Female', 26),
(1006, 'Kevin Kimani', 'IT', 67000, 'Male', 24),
(1007, 'Grace Achieng', 'HR', 76000, 'Female', 27),
(1008, 'Samuel Kiptoo', 'IT', 72000, 'Male', 28),
(1009, 'David Abdi', 'IT', 70000, 'Male', 28),
(1010, 'Halima Yusuf', 'HR', 88000, 'Female', 26);

-- Projects table
CREATE TABLE Projects (
 ProjectId INT PRIMARY KEY AUTO_INCREMENT,
 ProjectName VARCHAR(200) NOT NULL,
 EmployeeId INT,
 StartDate DATETIME,
 EndDate DATETIME,
 FOREIGN KEY (EmployeeId) REFERENCES Employee(EmployeeId)
);

INSERT INTO Projects (ProjectName, EmployeeId, StartDate, EndDate) VALUES 
('Develop Mobile App for M-Pesa Agents', 1003, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY)),
('Build HR Portal for Nairobi County', 1002, NOW(), DATE_ADD(NOW(), INTERVAL 45 DAY)),
('Set Up Servers at Konza Tech City', 1007, NOW(), DATE_ADD(NOW(), INTERVAL 45 DAY)),
('Fix Safaricom Data Center Issues', 1009, NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY)),
('Design Database for County Hospital', 1010, NOW(), DATE_ADD(NOW(), INTERVAL 15 DAY)),
('Develop eCitizen Chatbot', NULL, NOW(), DATE_ADD(NOW(), INTERVAL 10 DAY)),
('Migrate Banking System to Cloud', NULL, NOW(), DATE_ADD(NOW(), INTERVAL 5 DAY)),
('Create E-learning App for Schools', 1004, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY)),
('Fix Jambojet Online Booking System', 1001, NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY)),
('Build SACCO Loan Management System', 1008, NOW(), DATE_ADD(NOW(), INTERVAL 15 DAY)),
('Develop a Plugin for Local SME', NULL, NOW(), DATE_ADD(NOW(), INTERVAL 10 DAY));

-- Address table
CREATE TABLE Address (
 AddressId INT PRIMARY KEY AUTO_INCREMENT,
 EmployeeId INT,
 Country VARCHAR(50),
 County VARCHAR(50),
 City VARCHAR(50),
 FOREIGN KEY (EmployeeId) REFERENCES Employee(EmployeeId)
);

INSERT INTO Address (EmployeeId, Country, County, City) VALUES 
(1001, 'Kenya', 'Kisumu', 'Kisumu City'),
(1002, 'Kenya', 'Nairobi', 'Westlands'),
(1003, 'Kenya', 'Kiambu', 'Thika'),
(1004, 'Kenya', 'Mombasa', 'Nyali'),
(1005, 'Kenya', 'Nakuru', 'Nakuru Town'),
(1006, 'Kenya', 'Kakamega', 'Kakamega Town');

```
**INNER JOIN clause**

The **INNER JOIN** matches each row in one table with every row in other tables and allows you to query rows that contain columns from both tables.


```sql
-- Write a query to show which employees are currently assigned to projects.
SELECT E.EmployeeId, E.FullName, E.Department, P.ProjectName
FROM Employee E
INNER JOIN Projects P ON E.EmployeeId = P.EmployeeId;
```

**LEFT JOIN clause**

Returns all rows from the left table, irrespective of whether a matching row from the right table exists or not.

```sql
-- Write a query to show who which employee is still waiting for a project assignment.
SELECT E.EmployeeId, E.FullName, E.Department, P.ProjectName
FROM Employee E
LEFT JOIN Projects P ON E.EmployeeId = P.EmployeeId;
```

**RIGHT JOIN clause**

Returns all rows from the right table regardless of having matching rows from the left table or not.

```sql
-- Write a query to find which projects are waiting for staff allocation.
SELECT P.ProjectId, P.ProjectName, E.FullName, E.Department
FROM Employee E
RIGHT JOIN Projects P ON E.EmployeeId = P.EmployeeId;
```

