from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# ==================== DATABASE CONFIG ====================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Rachanjali062809',
    'database': 'inventory'
}

def get_db_connection():
    """Return a MySQL connection or None if fails."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ==================== HOME/DASHBOARD ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as count FROM Customer")
        customer_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM Product")
        product_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM Sale")
        sale_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM Supplier")
        supplier_count = cursor.fetchone()['count']

        supplier_count=supplier_count   
        
        cursor.execute("SELECT SUM(total_amount) as total FROM Sale")
        total_revenue = cursor.fetchone()['total'] or 0
        
        cursor.execute("""
            SELECT product_id, name, stock_level, reorder_level 
            FROM Product 
            WHERE stock_level <= reorder_level
            ORDER BY stock_level ASC
            LIMIT 5
        """)
        low_stock = cursor.fetchall()
        
        cursor.execute("""
            SELECT s.sale_id, c.name as customer_name, s.sale_date, s.total_amount
            FROM Sale s
            LEFT JOIN Customer c ON s.customer_id = c.customer_id
            ORDER BY s.sale_date DESC
            LIMIT 5
        """)
        recent_sales = cursor.fetchall()
    except Error as e:
        flash(f"Database query failed: {e}", "danger")
        return render_template('db_error.html')
    finally:
        cursor.close()
        conn.close()
    
    return render_template('dashboard.html', 
                           customer_count=customer_count,
                           product_count=product_count,
                           sale_count=sale_count,
                           total_revenue=total_revenue,
                           low_stock=low_stock,
                           recent_sales=recent_sales)

# ==================== CUSTOMERS CRUD ====================
@app.route('/customers')
def customers():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customer ORDER BY customer_id DESC")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for('customers'))
        
        cursor = None
        
        try:
            name = request.form['name']
            phone = request.form['phone_number']
            email = request.form['email']
            address = request.form['address']
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Customer (name, phone_number, email, address) 
                VALUES (%s, %s, %s, %s)
            """, (name, phone, email, address))
            conn.commit()
            
            print(f"✅ Customer added: {name}")
            print(f"✅ Rows affected: {cursor.rowcount}")
            
            flash('Customer added successfully!', 'success')
        except Error as e:
            flash(f"Error adding customer: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('customers'))
    
    return render_template('customer_form.html')

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('customers'))
    
    cursor = None
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone_number']
            email = request.form['email']
            address = request.form['address']
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Customer 
                SET name=%s, phone_number=%s, email=%s, address=%s 
                WHERE customer_id=%s
            """, (name, phone, email, address, id))
            conn.commit()
            
            flash('Customer updated successfully!', 'success')
        except Error as e:
            flash(f"Error updating customer: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('customers'))
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customer WHERE customer_id = %s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('customer_form.html', customer=customer)

@app.route('/customers/delete/<int:id>')
def delete_customer(id):
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('customers'))
    
    cursor = None
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customer WHERE customer_id = %s", (id,))
        conn.commit()
        flash('Customer deleted successfully!', 'success')
    except Error as e:
        flash(f"Error deleting customer: {e}", 'danger')
    finally:
        if cursor:
            cursor.close()
        conn.close()
    
    return redirect(url_for('customers'))

# ==================== PRODUCTS CRUD ====================
@app.route('/products')
def products():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product ORDER BY product_id DESC")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for('products'))
        
        cursor = None
        
        try:
            data = (
                request.form['name'],
                request.form['sku'],
                request.form['category'],
                request.form['price'],
                request.form['tax_rate'],
                request.form['stock_level'],
                request.form['reorder_level'],
                request.form['description']
            )
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Product 
                (name, SKU, category, price, tax_rate, stock_level, reorder_level, description) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            
            flash('Product added successfully!', 'success')
        except Error as e:
            flash(f"Error adding product: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('products'))
    
    return render_template('product_form.html')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('products'))
    
    cursor = None
    
    if request.method == 'POST':
        try:
            data = (
                request.form['name'],
                request.form['sku'],
                request.form['category'],
                request.form['price'],
                request.form['tax_rate'],
                request.form['stock_level'],
                request.form['reorder_level'],
                request.form['description'],
                id
            )
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Product SET name=%s, SKU=%s, category=%s, price=%s, tax_rate=%s,
                    stock_level=%s, reorder_level=%s, description=%s
                WHERE product_id=%s
            """, data)
            conn.commit()
            
            flash('Product updated successfully!', 'success')
        except Error as e:
            flash(f"Error updating product: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('products'))
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product WHERE product_id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('product_form.html', product=product)

@app.route('/products/delete/<int:id>')
def delete_product(id):
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('products'))
    
    cursor = None
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Product WHERE product_id = %s", (id,))
        conn.commit()
        flash('Product deleted successfully!', 'success')
    except Error as e:
        flash(f"Error deleting product: {e}", 'danger')
    finally:
        if cursor:
            cursor.close()
        conn.close()
    
    return redirect(url_for('products'))

# ==================== SALES ====================
@app.route('/sales')
def sales():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.sale_id, c.name as customer_name, e.name as employee_name, 
               s.sale_date, s.total_amount
        FROM Sale s
        LEFT JOIN Customer c ON s.customer_id = c.customer_id
        LEFT JOIN Employee e ON s.employee_id = e.employee_id
        ORDER BY s.sale_date DESC
    """)
    sales = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sales.html', sales=sales)
    # ==================== CREATE NEW SALE ====================
@app.route('/sales/add', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for('sales'))
        
        cursor = None
        
        try:
            cursor = conn.cursor()
            
            # Get form data
            customer_id = request.form.get('customer_id') or None
            employee_id = request.form['employee_id']
            product_ids = request.form.getlist('product_id[]')
            quantities = request.form.getlist('quantity[]')
            
            # Calculate total
            total_amount = 0
            sale_items = []
            
            for pid, qty in zip(product_ids, quantities):
                cursor.execute("SELECT price FROM Product WHERE product_id = %s", (pid,))
                price = cursor.fetchone()[0]
                total_amount += float(price) * int(qty)
                sale_items.append((pid, qty, price))
            
            # Insert Sale
            cursor.execute("""
                INSERT INTO Sale (customer_id, employee_id, total_amount) 
                VALUES (%s, %s, %s)
            """, (customer_id, employee_id, total_amount))
            sale_id = cursor.lastrowid
            
            # Insert Sale_Items (This triggers stock reduction!)
            for pid, qty, price in sale_items:
                cursor.execute("""
                    INSERT INTO Sale_Items (sale_id, product_id, quantity, price_at_time_of_sale)
                    VALUES (%s, %s, %s, %s)
                """, (sale_id, pid, qty, price))
            
            conn.commit()
            flash(f'Sale #{sale_id} created successfully! Stock updated automatically.', 'success')
        except Error as e:
            conn.rollback()
            flash(f"Error creating sale: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('sales'))
    
    # GET request - show form
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT customer_id, name FROM Customer ORDER BY name")
    customers = cursor.fetchall()
    
    cursor.execute("SELECT employee_id, name FROM Employee ORDER BY name")
    employees = cursor.fetchall()
    
    cursor.execute("SELECT product_id, name, price, stock_level FROM Product WHERE stock_level > 0 ORDER BY name")
    products = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('sale_form.html', customers=customers, employees=employees, products=products)

@app.route('/sales/view/<int:id>')
def view_sale(id):
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, c.name as customer_name, e.name as employee_name
        FROM Sale s
        LEFT JOIN Customer c ON s.customer_id = c.customer_id
        LEFT JOIN Employee e ON s.employee_id = e.employee_id
        WHERE s.sale_id = %s
    """, (id,))
    sale = cursor.fetchone()
    
    cursor.execute("""
        SELECT si.*, p.name as product_name
        FROM Sale_Items si
        JOIN Product p ON si.product_id = p.product_id
        WHERE si.sale_id = %s
    """, (id,))
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('sale_detail.html', sale=sale, items=items)

# ==================== REPORTS ====================
@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/reports/sales_summary')
def sales_summary():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE_FORMAT(sale_date, '%Y-%m') as month,
               COUNT(*) as total_sales,
               SUM(total_amount) as revenue
        FROM Sale
        GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
        ORDER BY month DESC
        LIMIT 12
    """)
    monthly_sales = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sales_summary.html', monthly_sales=monthly_sales)

@app.route('/reports/top_products')
def top_products():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.name, p.category, SUM(si.quantity) as total_sold, 
               SUM(si.quantity * si.price_at_time_of_sale) as revenue
        FROM Sale_Items si
        JOIN Product p ON si.product_id = p.product_id
        GROUP BY si.product_id
        ORDER BY total_sold DESC
        LIMIT 10
    """)
    top_products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('top_products.html', top_products=top_products)

    # ==================== USING STORED PROCEDURES ====================

@app.route('/reports/low_stock_procedure')
def low_stock_procedure():
    """Uses the get_low_stock_products() procedure"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('reports'))
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('get_low_stock_products')
        # Fetch results from the procedure
        for result in cursor.stored_results():
            low_stock = result.fetchall()
        
        return render_template('low_stock_report.html', low_stock=low_stock)
    except Error as e:
        flash(f"Error calling procedure: {e}", 'danger')
        return redirect(url_for('reports'))
    finally:
        cursor.close()
        conn.close()


@app.route('/reports/monthly_sales/<int:year>/<int:month>')
def monthly_sales_procedure(year, month):
    """Uses the get_monthly_sales_report() procedure"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('reports'))
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('get_monthly_sales_report', [year, month])
        for result in cursor.stored_results():
            sales_data = result.fetchall()
        
        return render_template('monthly_sales_report.html', 
                             sales_data=sales_data, 
                             year=year, 
                             month=month)
    except Error as e:
        flash(f"Error calling procedure: {e}", 'danger')
        return redirect(url_for('reports'))
    finally:
        cursor.close()
        conn.close()


@app.route('/customers/purchase_history/<int:customer_id>')
def customer_purchase_history(customer_id):
    """Uses the get_customer_purchase_history() procedure"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('customers'))
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Get customer name
        cursor.execute("SELECT name FROM Customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        
        # Call procedure
        cursor.callproc('get_customer_purchase_history', [customer_id])
        for result in cursor.stored_results():
            purchase_history = result.fetchall()
        
        return render_template('customer_history.html', 
                             customer=customer, 
                             purchases=purchase_history)
    except Error as e:
        flash(f"Error calling procedure: {e}", 'danger')
        return redirect(url_for('customers'))
    finally:
        cursor.close()
        conn.close()


# ==================== USING FUNCTIONS ====================

@app.route('/reports/revenue_calculator', methods=['GET', 'POST'])
def revenue_calculator():
    """Uses the calculate_revenue() function"""
    if request.method == 'POST':
        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for('reports'))
        
        cursor = conn.cursor()
        try:
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            
            cursor.execute("SELECT calculate_revenue(%s, %s) as revenue", (start_date, end_date))
            revenue = cursor.fetchone()[0]
            
            flash(f"Total Revenue from {start_date} to {end_date}: ₹{revenue:.2f}", 'success')
        except Error as e:
            flash(f"Error calculating revenue: {e}", 'danger')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('revenue_calculator.html')


@app.route('/products/stock_value/<int:product_id>')
def product_stock_value(product_id):
    """Uses the get_product_stock_value() function"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('products'))
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.*, get_product_stock_value(p.product_id) as stock_value
            FROM Product p
            WHERE p.product_id = %s
        """, (product_id,))
        product = cursor.fetchone()
        
        return render_template('product_stock_value.html', product=product)
    except Error as e:
        flash(f"Error: {e}", 'danger')
        return redirect(url_for('products'))
    finally:
        cursor.close()
        conn.close()


@app.route('/products/check_availability/<int:product_id>/<int:quantity>')
def check_availability(product_id, quantity):
    """Uses the check_product_availability() function"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT check_product_availability(%s, %s) as availability
        """, (product_id, quantity))
        availability = cursor.fetchone()[0]
        
        return jsonify({'availability': availability})
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/customers/lifetime_value/<int:customer_id>')
def customer_lifetime_value(customer_id):
    """Uses the calculate_customer_ltv() function"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('customers'))
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.*, calculate_customer_ltv(c.customer_id) as lifetime_value
            FROM Customer c
            WHERE c.customer_id = %s
        """, (customer_id,))
        customer = cursor.fetchone()
        
        flash(f"Customer Lifetime Value: ₹{customer['lifetime_value']:.2f}", 'info')
        return redirect(url_for('customers'))
    except Error as e:
        flash(f"Error: {e}", 'danger')
        return redirect(url_for('customers'))
    finally:
        cursor.close()
        conn.close()

# ==========================
# SUPPLIER MANAGEMENT ROUTES
# Add these routes to your app.py
# ==========================

# ==================== SUPPLIERS CRUD ====================
@app.route('/suppliers')
def suppliers():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    
    # Get all suppliers with product count and rating
    cursor.execute("""
        SELECT 
            s.*,
            COUNT(DISTINCT sp.product_id) as product_count,
            COUNT(DISTINCT sh.shipment_id) as total_shipments,
            calculate_supplier_rating(s.supplier_id) as rating
        FROM Supplier s
        LEFT JOIN Supplier_Products sp ON s.supplier_id = sp.supplier_id
        LEFT JOIN Supply_Shipment sh ON s.supplier_id = sh.supplier_id
        GROUP BY s.supplier_id
        ORDER BY s.supplier_id DESC
    """)
    suppliers = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for('suppliers'))
        
        cursor = None
        try:
            name = request.form['name']
            contact_info = request.form['contact_info']
            email = request.form['email']
            address = request.form['address']
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Supplier (name, contact_info, email, address) 
                VALUES (%s, %s, %s, %s)
            """, (name, contact_info, email, address))
            conn.commit()
            
            flash('Supplier added successfully!', 'success')
        except Error as e:
            flash(f"Error adding supplier: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('suppliers'))
    
    return render_template('supplier_form.html')

@app.route('/suppliers/edit/<int:id>', methods=['GET', 'POST'])
def edit_supplier(id):
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('suppliers'))
    
    cursor = None
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            contact_info = request.form['contact_info']
            email = request.form['email']
            address = request.form['address']
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Supplier 
                SET name=%s, contact_info=%s, email=%s, address=%s 
                WHERE supplier_id=%s
            """, (name, contact_info, email, address, id))
            conn.commit()
            
            flash('Supplier updated successfully!', 'success')
        except Error as e:
            flash(f"Error updating supplier: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('suppliers'))
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Supplier WHERE supplier_id = %s", (id,))
    supplier = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('supplier_form.html', supplier=supplier)

@app.route('/suppliers/delete/<int:id>')
def delete_supplier(id):
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('suppliers'))
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Supplier WHERE supplier_id = %s", (id,))
        conn.commit()
        flash('Supplier deleted successfully!', 'success')
    except Error as e:
        flash(f"Error deleting supplier: {e}", 'danger')
    finally:
        if cursor:
            cursor.close()
        conn.close()
    
    return redirect(url_for('suppliers'))

# ==================== SUPPLIER PRODUCTS ====================
@app.route('/suppliers/<int:supplier_id>/products')
def supplier_products(supplier_id):
    """View all products supplied by a specific supplier"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    
    # Get supplier details
    cursor.execute("SELECT * FROM Supplier WHERE supplier_id = %s", (supplier_id,))
    supplier = cursor.fetchone()
    
    # Use stored procedure to get supplier products
    try:
        cursor.callproc('get_supplier_products', [supplier_id])
        for result in cursor.stored_results():
            products = result.fetchall()
    except Error as e:
        flash(f"Error fetching products: {e}", 'danger')
        products = []
    
    cursor.close()
    conn.close()
    
    return render_template('supplier_products.html', supplier=supplier, products=products)

@app.route('/suppliers/<int:supplier_id>/products/add', methods=['GET', 'POST'])
def add_supplier_product(supplier_id):
    """Add a product to supplier's catalog"""
    if request.method == 'POST':
        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for('supplier_products', supplier_id=supplier_id))
        
        cursor = None
        try:
            product_id = request.form['product_id']
            supplier_sku = request.form['supplier_sku']
            supply_price = request.form['supply_price']
            minimum_order_quantity = request.form['minimum_order_quantity']
            lead_time_days = request.form['lead_time_days']
            is_preferred = 1 if 'is_preferred' in request.form else 0
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Supplier_Products 
                (supplier_id, product_id, supplier_sku, supply_price, 
                 minimum_order_quantity, lead_time_days, is_preferred) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (supplier_id, product_id, supplier_sku, supply_price, 
                  minimum_order_quantity, lead_time_days, is_preferred))
            conn.commit()
            
            flash('Product added to supplier catalog!', 'success')
        except Error as e:
            flash(f"Error adding product: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('supplier_products', supplier_id=supplier_id))
    
    # GET request - show form
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get supplier details
    cursor.execute("SELECT * FROM Supplier WHERE supplier_id = %s", (supplier_id,))
    supplier = cursor.fetchone()
    
    # Get products not yet linked to this supplier
    cursor.execute("""
        SELECT p.* FROM Product p
        WHERE p.product_id NOT IN (
            SELECT product_id FROM Supplier_Products 
            WHERE supplier_id = %s
        )
        ORDER BY p.name
    """, (supplier_id,))
    available_products = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('supplier_product_form.html', 
                         supplier=supplier, 
                         products=available_products)

@app.route('/suppliers/<int:supplier_id>/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_supplier_product(supplier_id, product_id):
    """Edit supplier product details"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('supplier_products', supplier_id=supplier_id))
    
    cursor = None
    
    if request.method == 'POST':
        try:
            supplier_sku = request.form['supplier_sku']
            supply_price = request.form['supply_price']
            minimum_order_quantity = request.form['minimum_order_quantity']
            lead_time_days = request.form['lead_time_days']
            is_preferred = 1 if 'is_preferred' in request.form else 0
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Supplier_Products 
                SET supplier_sku=%s, supply_price=%s, minimum_order_quantity=%s,
                    lead_time_days=%s, is_preferred=%s
                WHERE supplier_id=%s AND product_id=%s
            """, (supplier_sku, supply_price, minimum_order_quantity, 
                  lead_time_days, is_preferred, supplier_id, product_id))
            conn.commit()
            
            flash('Supplier product updated successfully!', 'success')
        except Error as e:
            flash(f"Error updating: {e}", 'danger')
        finally:
            if cursor:
                cursor.close()
            conn.close()
        
        return redirect(url_for('supplier_products', supplier_id=supplier_id))
    
    # GET request
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Supplier WHERE supplier_id = %s", (supplier_id,))
    supplier = cursor.fetchone()
    
    cursor.execute("""
        SELECT sp.*, p.name as product_name
        FROM Supplier_Products sp
        JOIN Product p ON sp.product_id = p.product_id
        WHERE sp.supplier_id = %s AND sp.product_id = %s
    """, (supplier_id, product_id))
    supplier_product = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('supplier_product_edit.html', 
                         supplier=supplier, 
                         supplier_product=supplier_product)

@app.route('/suppliers/<int:supplier_id>/products/<int:product_id>/delete')
def delete_supplier_product(supplier_id, product_id):
    """Remove product from supplier's catalog"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('supplier_products', supplier_id=supplier_id))
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM Supplier_Products 
            WHERE supplier_id = %s AND product_id = %s
        """, (supplier_id, product_id))
        conn.commit()
        flash('Product removed from supplier catalog!', 'success')
    except Error as e:
        flash(f"Error: {e}", 'danger')
    finally:
        if cursor:
            cursor.close()
        conn.close()
    
    return redirect(url_for('supplier_products', supplier_id=supplier_id))

# ==================== PRODUCT SUPPLIERS VIEW ====================
@app.route('/products/<int:product_id>/suppliers')
def product_suppliers(product_id):
    """View all suppliers for a specific product"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    
    # Get product details
    cursor.execute("SELECT * FROM Product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    
    # Use stored procedure to find best suppliers
    try:
        cursor.callproc('find_best_supplier', [product_id])
        for result in cursor.stored_results():
            suppliers = result.fetchall()
    except Error as e:
        flash(f"Error: {e}", 'danger')
        suppliers = []
    
    cursor.close()
    conn.close()
    
    return render_template('product_suppliers.html', product=product, suppliers=suppliers)

# ==================== REORDER MANAGEMENT ====================
@app.route('/inventory/reorder')
def reorder_list():
    """View products that need reordering with supplier info"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.callproc('get_reorder_list_with_suppliers')
        for result in cursor.stored_results():
            reorder_items = result.fetchall()
    except Error as e:
        flash(f"Error: {e}", 'danger')
        reorder_items = []
    
    cursor.close()
    conn.close()
    
    return render_template('reorder_list.html', items=reorder_items)

# ==================== SUPPLIER COMPARISON ====================
@app.route('/suppliers/compare/<int:product_id>')
def compare_suppliers(product_id):
    """Compare all suppliers for a specific product"""
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return render_template('db_error.html')
    
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    
    cursor.execute("""
        SELECT 
            s.supplier_id,
            s.name as supplier_name,
            s.contact_info,
            s.email,
            sp.supply_price,
            sp.minimum_order_quantity,
            sp.lead_time_days,
            sp.is_preferred,
            sp.last_supply_date,
            calculate_supplier_rating(s.supplier_id) as rating,
            COUNT(sh.shipment_id) as total_shipments
        FROM Supplier_Products sp
        JOIN Supplier s ON sp.supplier_id = s.supplier_id
        LEFT JOIN Supply_Shipment sh ON s.supplier_id = sh.supplier_id
        WHERE sp.product_id = %s
        GROUP BY s.supplier_id
        ORDER BY sp.is_preferred DESC, sp.supply_price ASC
    """, (product_id,))
    suppliers = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('supplier_comparison.html', product=product, suppliers=suppliers)

if __name__ == '__main__':
    app.run(debug=True, port=5000)