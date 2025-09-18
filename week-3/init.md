## 🎯 Hands-on Class Activity

To Mark the beginning of a transaction
```sql
START TRANSACTION
```
Apply the changes of a transaction to the database.
```sql
COMMIT
```
Undo the changes of a transaction by reverting the database to the state before the transaction starts.
```sql
ROLLBACK
```
To instruct MySQL to not start a transaction implicitly and commit the changes automatically
```sql
SET autocommit = OFF;
```
### Transactions example
```sql
CREATE DATABASE stadium;
USE stadium;
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255)
);
```
### COMMIT Example
```sql
START TRANSACTION;

INSERT INTO users (id, username) 
VALUES (1, 'peter');

UPDATE users 
SET email = 'peter@mail.com' 
WHERE id = 1;
COMMIT;
```
Select data from the users table
```sql
SELECT * FROM users;
```
### ROLLBACK Example
```sql
START TRANSACTION;
INSERT INTO users (id, username) 
VALUES (2, 'sharon');

UPDATE users 
SET email = 'sharon@mail.com' 
WHERE id = 2;
ROLLBACK;
```
Select data from the users table
```sql
SELECT * FROM users;
```
### Aggregate Functions
**AVG() function** calculates the average value of a set of values
```sql
SELECT 
    AVG(buyPrice) avg_buy_price
FROM 
    products;
```
**COUNT() function** function returns the number of the values in a set.
```sql
SELECT 
    COUNT(*) AS total
FROM 
    products;
```
**SUM() function** returns the sum of values in a set.
```sql
SELECT 
    productCode, 
    SUM(priceEach * quantityOrdered) total
FROM
    orderDetails
GROUP BY productCode
ORDER BY total DESC;
```
**MAX() function** returns the maximum value in a set.
```sql
SELECT 
     MAX(buyPrice) highest_price
FROM 
     products;
```
**MIN() function** returns the minimum value in a set of values
```sql
SELECT 
    MIN(buyPrice) lowest_price
FROM 
    products;
```
### GROUP BY Examples
To group the order statuses:
```sql
SELECT 
  status 
FROM 
  orders 
GROUP BY 
  status;
```
To obtain the number of orders in each status:
```sql
SELECT 
  status, 
  COUNT(*) 
FROM 
  orders 
GROUP BY 
  status;
```
To get total amount of each order:
```sql
SELECT 
  orderNumber, 
  SUM(quantityOrdered * priceEach) AS total 
FROM 
  orderdetails 
GROUP BY 
  orderNumber;
```
#### HAVING Clause
Allows you to apply a condition to the groups returned by the GROUP BY clause and only include groups that meet the specified condition.
To find which order has total sales greater than 1000:
```sql
SELECT 
  ordernumber, 
  SUM(quantityOrdered) AS itemsCount, 
  SUM(priceeach * quantityOrdered) AS total 
FROM 
  orderdetails 
GROUP BY 
  ordernumber 
HAVING 
  total > 1000;
```
