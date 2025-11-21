-- ==========================
-- TRIGGERS, PROCEDURES & FUNCTIONS
-- Smart Inventory Management System
-- ==========================

USE inventory;

DELIMITER $$

-- ==========================
-- TRIGGER 1: Auto Update Stock After Sale
-- ==========================
DROP TRIGGER IF EXISTS update_stock_after_sale$$
CREATE TRIGGER update_stock_after_sale
AFTER INSERT ON Sale_Items
FOR EACH ROW
BEGIN
    UPDATE Product 
    SET stock_level = stock_level - NEW.quantity
    WHERE product_id = NEW.product_id;
END$$

-- ==========================
-- TRIGGER 2: Restore Stock After Return
-- ==========================
DROP TRIGGER IF EXISTS restore_stock_after_return$$
CREATE TRIGGER restore_stock_after_return
AFTER INSERT ON Return_Items
FOR EACH ROW
BEGIN
    UPDATE Product 
    SET stock_level = stock_level + NEW.quantity
    WHERE product_id = NEW.product_id;
END$$

-- ==========================
-- TRIGGER 3: Auto Update Bill Status After Payment
-- ==========================
DROP TRIGGER IF EXISTS update_bill_status_after_payment$$
CREATE TRIGGER update_bill_status_after_payment
AFTER INSERT ON Payment
FOR EACH ROW
BEGIN
    DECLARE bill_total DECIMAL(10,2);
    DECLARE paid_amount DECIMAL(10,2);
    
    SELECT total_amount INTO bill_total 
    FROM Bill WHERE bill_id = NEW.bill_id;
    
    SELECT SUM(amount) INTO paid_amount 
    FROM Payment WHERE bill_id = NEW.bill_id;
    
    IF paid_amount >= bill_total THEN
        UPDATE Bill SET status = 'PAID' WHERE bill_id = NEW.bill_id;
    ELSE
        UPDATE Bill SET status = 'PENDING' WHERE bill_id = NEW.bill_id;
    END IF;
END$$

-- ==========================
-- TRIGGER 4: Increase Stock After Shipment Delivery
-- ==========================
DROP TRIGGER IF EXISTS increase_stock_on_delivery$$
CREATE TRIGGER increase_stock_on_delivery
AFTER UPDATE ON Supply_Shipment
FOR EACH ROW
BEGIN
    IF NEW.status = 'DELIVERED' AND OLD.status != 'DELIVERED' THEN
        UPDATE Product p
        INNER JOIN Shipment_Items si ON p.product_id = si.product_id
        SET p.stock_level = p.stock_level + si.quantity
        WHERE si.shipment_id = NEW.shipment_id;
    END IF;
END$$

-- ==========================
-- PROCEDURE 1: Get Monthly Sales Report
-- ==========================
DROP PROCEDURE IF EXISTS get_monthly_sales_report$$
CREATE PROCEDURE get_monthly_sales_report(IN report_year INT, IN report_month INT)
BEGIN
    SELECT 
        DATE(s.sale_date) as sale_date,
        COUNT(DISTINCT s.sale_id) as total_sales,
        SUM(s.total_amount) as daily_revenue,
        AVG(s.total_amount) as avg_sale_amount
    FROM Sale s
    WHERE YEAR(s.sale_date) = report_year 
    AND MONTH(s.sale_date) = report_month
    GROUP BY DATE(s.sale_date)
    ORDER BY sale_date;
END$$

-- ==========================
-- PROCEDURE 2: Get Low Stock Products
-- ==========================
DROP PROCEDURE IF EXISTS get_low_stock_products$$
CREATE PROCEDURE get_low_stock_products()
BEGIN
    SELECT 
        product_id,
        name,
        SKU,
        category,
        stock_level,
        reorder_level,
        (reorder_level - stock_level) as qty_to_order
    FROM Product
    WHERE stock_level <= reorder_level
    ORDER BY stock_level ASC;
END$$

-- ==========================
-- PROCEDURE 3: Process Customer Refund
-- ==========================
DROP PROCEDURE IF EXISTS process_refund$$
CREATE PROCEDURE process_refund(
    IN p_return_id INT,
    IN p_refund_amount DECIMAL(10,2),
    IN p_refund_method VARCHAR(50)
)
BEGIN
    DECLARE refund_exists INT;
    
    SELECT COUNT(*) INTO refund_exists 
    FROM Refund WHERE return_id = p_return_id;
    
    IF refund_exists = 0 THEN
        INSERT INTO Refund (return_id, amount, refund_method, status)
        VALUES (p_return_id, p_refund_amount, p_refund_method, 'COMPLETED');
        
        UPDATE Sale_Return 
        SET status = 'APPROVED' 
        WHERE return_id = p_return_id;
        
        SELECT 'Refund processed successfully' as message;
    ELSE
        SELECT 'Refund already exists for this return' as message;
    END IF;
END$$

-- ==========================
-- PROCEDURE 4: Get Customer Purchase History
-- ==========================
DROP PROCEDURE IF EXISTS get_customer_purchase_history$$
CREATE PROCEDURE get_customer_purchase_history(IN p_customer_id INT)
BEGIN
    SELECT 
        s.sale_id,
        s.sale_date,
        s.total_amount,
        GROUP_CONCAT(p.name SEPARATOR ', ') as products_purchased,
        SUM(si.quantity) as total_items
    FROM Sale s
    JOIN Sale_Items si ON s.sale_id = si.sale_id
    JOIN Product p ON si.product_id = p.product_id
    WHERE s.customer_id = p_customer_id
    GROUP BY s.sale_id
    ORDER BY s.sale_date DESC;
END$$

-- ==========================
-- FUNCTION 1: Calculate Total Revenue for Date Range
-- ==========================
DROP FUNCTION IF EXISTS calculate_revenue$$
CREATE FUNCTION calculate_revenue(start_date DATE, end_date DATE)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total_revenue DECIMAL(10,2);
    
    SELECT COALESCE(SUM(total_amount), 0) INTO total_revenue
    FROM Sale
    WHERE sale_date BETWEEN start_date AND end_date;
    
    RETURN total_revenue;
END$$

-- ==========================
-- FUNCTION 2: Get Product Stock Value
-- ==========================
DROP FUNCTION IF EXISTS get_product_stock_value$$
CREATE FUNCTION get_product_stock_value(p_product_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE stock_value DECIMAL(10,2);
    
    SELECT (stock_level * price) INTO stock_value
    FROM Product
    WHERE product_id = p_product_id;
    
    RETURN COALESCE(stock_value, 0);
END$$

-- ==========================
-- FUNCTION 3: Check Product Availability
-- ==========================
DROP FUNCTION IF EXISTS check_product_availability$$
CREATE FUNCTION check_product_availability(p_product_id INT, p_quantity INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE current_stock INT;
    
    SELECT stock_level INTO current_stock
    FROM Product
    WHERE product_id = p_product_id;
    
    IF current_stock >= p_quantity THEN
        RETURN 'AVAILABLE';
    ELSEIF current_stock > 0 THEN
        RETURN 'LIMITED_STOCK';
    ELSE
        RETURN 'OUT_OF_STOCK';
    END IF;
END$$

-- ==========================
-- FUNCTION 4: Calculate Customer Lifetime Value
-- ==========================
DROP FUNCTION IF EXISTS calculate_customer_ltv$$
CREATE FUNCTION calculate_customer_ltv(p_customer_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE lifetime_value DECIMAL(10,2);
    
    SELECT COALESCE(SUM(total_amount), 0) INTO lifetime_value
    FROM Sale
    WHERE customer_id = p_customer_id;
    
    RETURN lifetime_value;
END$$

DELIMITER ;

-- ==========================
-- VERIFICATION: Test the procedures and functions
-- ==========================

-- Test Procedure: Get low stock products
CALL get_low_stock_products();

-- Test Procedure: Get monthly sales report for October 2025
CALL get_monthly_sales_report(2025, 10);

-- Test Function: Calculate revenue for October 2025
SELECT calculate_revenue('2025-10-01', '2025-10-31') as october_revenue;

-- Test Function: Check product availability
SELECT 
    product_id, 
    name, 
    stock_level,
    check_product_availability(product_id, 10) as availability
FROM Product
LIMIT 5;

-- Test Function: Get product stock value
SELECT 
    product_id, 
    name, 
    stock_level, 
    price,
    get_product_stock_value(product_id) as stock_value
FROM Product
LIMIT 5;

-- Test Function: Customer lifetime value
SELECT 
    c.customer_id,
    c.name,
    calculate_customer_ltv(c.customer_id) as lifetime_value
FROM Customer c
LIMIT 5;