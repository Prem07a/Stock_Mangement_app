CREATE DATABASE stock_market_db;

USE stock_market_db;

CREATE TABLE users (
  user_id INT NOT NULL AUTO_INCREMENT,
  full_name VARCHAR(255) NOT NULL,
  pan_number VARCHAR(10) NOT NULL UNIQUE,
  aadhar_number VARCHAR(12) NOT NULL UNIQUE,
  phone_number VARCHAR(10) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE wallets (
  wallet_id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  balance DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (wallet_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE companies (
  company_id INT NOT NULL AUTO_INCREMENT,
  company_name VARCHAR(255) NOT NULL,
  sector VARCHAR(255) NOT NULL,
  stock_price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (company_id)
);

CREATE TABLE shares (
  share_id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  company_id INT NOT NULL,
  shares_owned INT NOT NULL,
  PRIMARY KEY (share_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Insert data for 5 users
INSERT INTO users (full_name, pan_number, aadhar_number, phone_number, password)
VALUES
('Amit Kumar', 'ABCDEF12', '123456789012', '9876543210', 'password1'),
('Sneha Gupta', 'FGHIJ5678', '345678901234', '8765432109', 'password2'),
('Rajesh Verma', 'LMNOP1234', '5678901234', '7654321098', 'password3'),
('Priya Sharma', 'UVWXYZ5678', '7890123456', '6543210987', 'password4'),
('Ravi Singh', 'PQRSTU1234', '8900234567', '5432109876', 'password5');

-- Insert balance data for 5 users
INSERT INTO wallets (user_id, balance)
VALUES
(1, 10000.00), -- User 1 (Amit Kumar)
(2, 9500.00),  -- User 2 (Sneha Gupta)
(3, 11000.00), -- User 3 (Rajesh Verma)
(4, 8500.00),  -- User 4 (Priya Sharma)
(5, 10250.00); -- User 5 (Ravi Singh);

-- Add companies
INSERT INTO companies (company_name, sector, stock_price)
VALUES
  ('Tata Motors', 'Automobile', 100.00),
  ('Infosys', 'Information Technology', 50.00),
  ('Reliance Industries', 'Conglomerate', 75.00),
  ('ICICI Bank', 'Banking', 45.00),
  ('HDFC Ltd', 'Finance', 60.00);

-- User 1 (Amit Kumar)
INSERT INTO shares (user_id, company_id, shares_owned)
VALUES (1, 1, 50),
       (1, 2, 75),
       (1, 4, 30);

-- User 2 (Sneha Gupta)
INSERT INTO shares (user_id, company_id, shares_owned)
VALUES (2, 2, 60),
       (2, 3, 90),
       (2, 5, 40);

-- User 3 (Rajesh Verma)
INSERT INTO shares (user_id, company_id, shares_owned)
VALUES (3, 1, 75),
       (3, 4, 20),
       (3, 5, 50);

-- User 4 (Priya Sharma)
INSERT INTO shares (user_id, company_id, shares_owned)
VALUES (4, 3, 100),
       (4, 5, 70);

-- User 5 (Ravi Singh)
INSERT INTO shares (user_id, company_id, shares_owned)
VALUES (5, 1, 40),
       (5, 2, 85),
       (5, 3, 60);
