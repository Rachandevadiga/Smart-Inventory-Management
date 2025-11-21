-- ==========================
-- SAMPLE DATA INSERT STATEMENTS
-- Smart Inventory Management System
-- ==========================

USE inventory;

-- ==========================
-- CLEAR ALL EXISTING DATA
-- ==========================
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE Payment_To_Supplier;
TRUNCATE TABLE Supplier_Bill;
TRUNCATE TABLE Shipment_Items;
TRUNCATE TABLE Supply_Shipment;
TRUNCATE TABLE Supplier;
TRUNCATE TABLE Return_Items;
TRUNCATE TABLE Refund;
TRUNCATE TABLE Sale_Return;
TRUNCATE TABLE Sale_Items;
TRUNCATE TABLE Payment;
TRUNCATE TABLE Bill;
TRUNCATE TABLE Sale;
TRUNCATE TABLE Product;
TRUNCATE TABLE Customer;
TRUNCATE TABLE Employee;

SET FOREIGN_KEY_CHECKS = 1;

-- ==========================
-- 1. CUSTOMERS
-- ==========================
INSERT INTO Customer (customer_id, name, phone_number, email, address) VALUES
(1, 'Ramesh Kumar', '9876543210', 'ramesh@email.com', '123 MG Road, Bangalore'),
(2, 'Anita Sharma', '9876543211', 'anita@email.com', '456 Park Street, Delhi'),
(3, 'John Doe', '9876543212', 'john@email.com', '789 Brigade Road, Bangalore'),
(4, 'Priya Patel', '9876543213', 'priya@email.com', '321 Anna Salai, Chennai'),
(5, 'Vikram Singh', '9876543214', 'vikram@email.com', '654 Linking Road, Mumbai');

-- ==========================
-- 2. EMPLOYEES
-- ==========================
INSERT INTO Employee (employee_id, name, role, phone_number, salary, hire_date) VALUES
(1, 'Suresh Manager', 'Manager', '8765432100', 50000.00, '2023-01-15'),
(2, 'Lakshmi Cashier', 'Cashier', '8765432101', 25000.00, '2023-03-20'),
(3, 'Ravi Stock', 'Stock Keeper', '8765432102', 22000.00, '2023-05-10'),
(4, 'Kavita Sales', 'Sales Executive', '8765432103', 28000.00, '2023-07-01'),
(5, 'Amit Helper', 'Store Helper', '8765432104', 18000.00, '2024-01-15');

-- ==========================
-- 3. SUPPLIERS
-- ==========================
INSERT INTO Supplier (supplier_id, name, contact_info, email, address) VALUES
(1, 'TechWorld Distributors', '9123456780', 'contact@techworld.com', 'Whitefield, Bangalore'),
(2, 'Electronics Hub', '9123456781', 'info@electrohub.com', 'Nehru Place, Delhi'),
(3, 'Office Supplies Co', '9123456782', 'sales@officesupply.com', 'T Nagar, Chennai'),
(4, 'Smart Gadgets Ltd', '9123456783', 'orders@smartgadgets.com', 'Andheri, Mumbai'),
(5, 'Mega Wholesale', '9123456784', 'support@megawholesale.com', 'Sector 18, Noida');

-- ==========================
-- 4. PRODUCTS
-- ==========================
INSERT INTO Product (product_id, name, SKU, category, price, tax_rate, stock_level, reorder_level, description) VALUES
(1, 'Laptop Bag', 'LB001', 'Accessories', 750.00, 18.00, 50, 10, 'Premium quality laptop bag'),
(2, 'Wireless Mouse', 'WM002', 'Electronics', 490.10, 18.00, 100, 20, 'Ergonomic wireless mouse'),
(3, 'Keyboard', 'KB003', 'Electronics', 980.75, 18.00, 75, 15, 'Mechanical keyboard RGB'),
(4, 'USB Cable', 'UC004', 'Accessories', 150.00, 12.00, 200, 50, 'USB Type-C cable 1m'),
(5, 'Phone Case', 'PC005', 'Accessories', 299.00, 12.00, 150, 30, 'Protective phone case'),
(6, 'Headphones', 'HP006', 'Electronics', 1299.00, 18.00, 60, 10, 'Noise cancelling headphones'),
(7, 'Power Bank', 'PB007', 'Electronics', 899.00, 18.00, 80, 20, '10000mAh power bank'),
(8, 'Screen Guard', 'SG008', 'Accessories', 199.00, 12.00, 120, 25, 'Tempered glass screen protector'),
(9, 'Webcam', 'WC009', 'Electronics', 1899.00, 18.00, 40, 10, 'HD webcam with mic'),
(10, 'Pen Drive 32GB', 'PD010', 'Electronics', 399.00, 18.00, 90, 20, '32GB USB 3.0 pen drive');

-- ==========================
-- 5. SALES
-- ==========================
INSERT INTO Sale (sale_id, customer_id, employee_id, sale_date, total_amount) VALUES
(1, 1, 2, '2025-10-01 10:30:00', 1650.00),
(2, 2, 2, '2025-10-02 14:15:00', 2695.55),
(3, 3, 4, '2025-10-03 11:20:00', 1156.49),
(4, 4, 2, '2025-10-04 16:45:00', 1533.00),
(5, 5, 4, '2025-10-05 09:30:00', 2358.00);

-- ==========================
-- 6. SALE ITEMS
-- ==========================
INSERT INTO Sale_Items (sale_id, product_id, quantity, price_at_time_of_sale) VALUES
(1, 1, 2, 750.00),   -- 2 Laptop Bags
(1, 4, 1, 150.00),   -- 1 USB Cable
(2, 2, 5, 490.10),   -- 5 Wireless Mouse
(2, 5, 2, 299.00),   -- 2 Phone Cases
(3, 3, 1, 980.75),   -- 1 Keyboard
(3, 8, 1, 199.00),   -- 1 Screen Guard
(4, 6, 1, 1299.00),  -- 1 Headphones
(4, 8, 1, 199.00),   -- 1 Screen Guard
(5, 7, 2, 899.00),   -- 2 Power Banks
(5, 9, 1, 1899.00);  -- 1 Webcam

-- ==========================
-- 7. BILLS
-- ==========================
INSERT INTO Bill (bill_id, sale_id, bill_date, status, total_tax, total_amount) VALUES
(1, 1, '2025-10-01 10:30:00', 'PAID', 280.80, 1930.80),
(2, 2, '2025-10-02 14:15:00', 'PAID', 441.92, 3137.47),
(3, 3, '2025-10-03 11:20:00', 'PAID', 188.12, 1344.61),
(4, 4, '2025-10-04 16:45:00', 'PAID', 257.64, 1790.64),
(5, 5, '2025-10-05 09:30:00', 'PENDING', 403.64, 2761.64);

-- ==========================
-- 8. PAYMENTS
-- ==========================
INSERT INTO Payment (payment_id, bill_id, payment_date, amount, payment_method, transaction_id) VALUES
(1, 1, '2025-10-01 10:32:00', 1930.80, 'CASH', NULL),
(2, 2, '2025-10-02 14:17:00', 3137.47, 'CARD', 'TXN20251002001'),
(3, 3, '2025-10-03 11:22:00', 1344.61, 'UPI', 'UPI20251003001'),
(4, 4, '2025-10-04 16:47:00', 1790.64, 'NETBANKING', 'NET20251004001');

-- ==========================
-- 9. SALE RETURNS
-- ==========================
INSERT INTO Sale_Return (return_id, sale_id, return_date, reason, status) VALUES
(1, 2, '2025-10-05 10:00:00', 'Product Defective - Mouse not working', 'APPROVED'),
(2, 3, '2025-10-06 15:30:00', 'Wrong Item Delivered', 'APPROVED'),
(3, 1, '2025-10-07 12:00:00', 'Customer changed mind', 'PENDING');

-- ==========================
-- 10. RETURN ITEMS
-- ==========================
INSERT INTO Return_Items (return_id, product_id, quantity) VALUES
(1, 2, 1),  -- 1 Wireless Mouse returned
(2, 3, 1),  -- 1 Keyboard returned
(3, 1, 1);  -- 1 Laptop Bag returned

-- ==========================
-- 11. REFUNDS
-- ==========================
INSERT INTO Refund (refund_id, return_id, refund_date, amount, refund_method, status) VALUES
(1, 1, '2025-10-05 10:30:00', 578.32, 'UPI', 'COMPLETED'),
(2, 2, '2025-10-06 16:00:00', 1156.49, 'CARD', 'COMPLETED');

-- ==========================
-- 12. SUPPLY SHIPMENTS
-- ==========================
INSERT INTO Supply_Shipment (shipment_id, supplier_id, shipment_date, expected_delivery, status, total_amount) VALUES
(1, 1, '2025-09-25 09:00:00', '2025-09-28', 'DELIVERED', 45000.00),
(2, 2, '2025-10-01 10:00:00', '2025-10-05', 'IN_TRANSIT', 30000.00),
(3, 3, '2025-10-03 11:30:00', '2025-10-07', 'ORDERED', 15000.00),
(4, 4, '2025-10-05 14:00:00', '2025-10-10', 'ORDERED', 25000.00);

-- ==========================
-- 13. SHIPMENT ITEMS
-- ==========================
INSERT INTO Shipment_Items (shipment_id, product_id, quantity, cost_per_item) VALUES
(1, 1, 50, 450.00),   -- 50 Laptop Bags @ 450
(1, 2, 100, 250.00),  -- 100 Wireless Mouse @ 250
(2, 3, 75, 600.00),   -- 75 Keyboards @ 600
(2, 6, 60, 800.00),   -- 60 Headphones @ 800
(3, 4, 200, 75.00),   -- 200 USB Cables @ 75
(3, 5, 150, 150.00),  -- 150 Phone Cases @ 150
(4, 7, 80, 550.00),   -- 80 Power Banks @ 550
(4, 9, 40, 1200.00);  -- 40 Webcams @ 1200

-- ==========================
-- 14. SUPPLIER BILLS
-- ==========================
INSERT INTO Supplier_Bill (bill_id, shipment_id, bill_date, total_amount, status) VALUES
(1, 1, '2025-09-28 10:00:00', 45000.00, 'PAID'),
(2, 2, '2025-10-05 12:00:00', 30000.00, 'UNPAID'),
(3, 3, '2025-10-07 14:00:00', 15000.00, 'UNPAID'),
(4, 4, '2025-10-10 16:00:00', 25000.00, 'UNPAID');

-- ==========================
-- 15. PAYMENTS TO SUPPLIERS
-- ==========================
INSERT INTO Payment_To_Supplier (payment_id, bill_id, payment_date, amount, payment_method, transaction_reference) VALUES
(1, 1, '2025-09-30 11:00:00', 45000.00, 'BANK_TRANSFER', 'REF2025093001'),
(2, 2, '2025-10-06 10:00:00', 15000.00, 'BANK_TRANSFER', 'REF2025100601');

-- ==========================
-- VERIFICATION QUERIES
-- ==========================
SELECT 'Customers' as TableName, COUNT(*) as RecordCount FROM Customer
UNION ALL
SELECT 'Employees', COUNT(*) FROM Employee
UNION ALL
SELECT 'Suppliers', COUNT(*) FROM Supplier
UNION ALL
SELECT 'Products', COUNT(*) FROM Product
UNION ALL
SELECT 'Sales', COUNT(*) FROM Sale
UNION ALL
SELECT 'Sale_Items', COUNT(*) FROM Sale_Items
UNION ALL
SELECT 'Bills', COUNT(*) FROM Bill
UNION ALL
SELECT 'Payments', COUNT(*) FROM Payment
UNION ALL
SELECT 'Sale_Returns', COUNT(*) FROM Sale_Return
UNION ALL
SELECT 'Return_Items', COUNT(*) FROM Return_Items
UNION ALL
SELECT 'Refunds', COUNT(*) FROM Refund
UNION ALL
SELECT 'Supply_Shipments', COUNT(*) FROM Supply_Shipment
UNION ALL
SELECT 'Shipment_Items', COUNT(*) FROM Shipment_Items
UNION ALL
SELECT 'Supplier_Bills', COUNT(*) FROM Supplier_Bill
UNION ALL
SELECT 'Payments_To_Supplier', COUNT(*) FROM Payment_To_Supplier;