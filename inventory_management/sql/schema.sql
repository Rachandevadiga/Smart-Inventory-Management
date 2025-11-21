-- ==========================
-- SMART INVENTORY MANAGEMENT SYSTEM
-- Complete Database Schema
-- ==========================

USE inventory;

-- ==========================
-- DROP TABLES (for clean reruns)
-- ==========================
DROP TABLE IF EXISTS Payment_To_Supplier;
DROP TABLE IF EXISTS Supplier_Bill;
DROP TABLE IF EXISTS Shipment_Items;
DROP TABLE IF EXISTS Supply_Shipment;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Return_Items;
DROP TABLE IF EXISTS Refund;
DROP TABLE IF EXISTS Sale_Return;
DROP TABLE IF EXISTS Sale_Items;
DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Bill;
DROP TABLE IF EXISTS Sale;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Employee;

-- ==========================
-- 1. CUSTOMER TABLE
-- ==========================
CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) UNIQUE,
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- 2. EMPLOYEE TABLE
-- ==========================
CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15),
    salary DECIMAL(10,2),
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- 3. PRODUCT TABLE (Inventory)
-- ==========================
CREATE TABLE Product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    SKU VARCHAR(50) UNIQUE,
    category VARCHAR(50),
    price DECIMAL(10,2) CHECK (price >= 0),
    tax_rate DECIMAL(5,2) DEFAULT 0,
    stock_level INT CHECK (stock_level >= 0),
    reorder_level INT DEFAULT 10,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- 4. SUPPLIER TABLE
-- ==========================
CREATE TABLE Supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100),
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- 5. SALE TABLE
-- ==========================
CREATE TABLE Sale (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    employee_id INT NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) CHECK (total_amount >= 0),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE SET NULL,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id) ON DELETE CASCADE
);

-- ==========================
-- 6. SALE_ITEMS TABLE (Sale details)
-- ==========================
CREATE TABLE Sale_Items (
    sale_id INT,
    product_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    price_at_time_of_sale DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (quantity * price_at_time_of_sale) STORED,
    PRIMARY KEY (sale_id, product_id),
    FOREIGN KEY (sale_id) REFERENCES Sale(sale_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

-- ==========================
-- 7. BILL TABLE
-- ==========================
CREATE TABLE Bill (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT UNIQUE NOT NULL,
    bill_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('PAID', 'UNPAID', 'PENDING') DEFAULT 'PENDING',
    total_tax DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES Sale(sale_id) ON DELETE CASCADE
);

-- ==========================
-- 8. PAYMENT TABLE
-- ==========================
CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    payment_method ENUM('CASH', 'CARD', 'UPI', 'NETBANKING') NOT NULL,
    transaction_id VARCHAR(100),
    FOREIGN KEY (bill_id) REFERENCES Bill(bill_id) ON DELETE CASCADE
);

-- ==========================
-- 9. SALE_RETURN TABLE
-- ==========================
CREATE TABLE Sale_Return (
    return_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    return_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(255),
    status ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING',
    FOREIGN KEY (sale_id) REFERENCES Sale(sale_id) ON DELETE CASCADE
);

-- ==========================
-- 10. RETURN_ITEMS TABLE
-- ==========================
CREATE TABLE Return_Items (
    return_id INT,
    product_id INT,
    quantity INT CHECK (quantity > 0),
    PRIMARY KEY (return_id, product_id),
    FOREIGN KEY (return_id) REFERENCES Sale_Return(return_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

-- ==========================
-- 11. REFUND TABLE
-- ==========================
CREATE TABLE Refund (
    refund_id INT AUTO_INCREMENT PRIMARY KEY,
    return_id INT UNIQUE NOT NULL,
    refund_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    refund_method ENUM('CASH', 'CARD', 'UPI', 'BANK_TRANSFER'),
    status ENUM('PENDING', 'COMPLETED', 'FAILED') DEFAULT 'PENDING',
    FOREIGN KEY (return_id) REFERENCES Sale_Return(return_id) ON DELETE CASCADE
);

-- ==========================
-- 12. SUPPLY_SHIPMENT TABLE
-- ==========================
CREATE TABLE Supply_Shipment (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    shipment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expected_delivery DATE,
    status ENUM('ORDERED', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED') DEFAULT 'ORDERED',
    total_amount DECIMAL(10,2),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id) ON DELETE CASCADE
);

-- ==========================
-- 13. SHIPMENT_ITEMS TABLE
-- ==========================
CREATE TABLE Shipment_Items (
    shipment_id INT,
    product_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    cost_per_item DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (quantity * cost_per_item) STORED,
    PRIMARY KEY (shipment_id, product_id),
    FOREIGN KEY (shipment_id) REFERENCES Supply_Shipment(shipment_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

-- ==========================
-- 14. SUPPLIER_BILL TABLE
-- ==========================
CREATE TABLE Supplier_Bill (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    shipment_id INT UNIQUE NOT NULL,
    bill_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('UNPAID', 'PARTIALLY_PAID', 'PAID') DEFAULT 'UNPAID',
    FOREIGN KEY (shipment_id) REFERENCES Supply_Shipment(shipment_id) ON DELETE CASCADE
);

-- ==========================
-- 15. PAYMENT_TO_SUPPLIER TABLE
-- ==========================
CREATE TABLE Payment_To_Supplier (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    payment_method ENUM('CASH', 'CHEQUE', 'BANK_TRANSFER', 'UPI'),
    transaction_reference VARCHAR(100),
    FOREIGN KEY (bill_id) REFERENCES Supplier_Bill(bill_id) ON DELETE CASCADE
);

-- ==========================
-- INDEXES for Performance
-- ==========================
CREATE INDEX idx_sale_date ON Sale(sale_date);
CREATE INDEX idx_customer_phone ON Customer(phone_number);
CREATE INDEX idx_product_sku ON Product(SKU);
CREATE INDEX idx_bill_status ON Bill(status);
CREATE INDEX idx_shipment_status ON Supply_Shipment(status);