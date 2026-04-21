"""Reports database model and operations"""
import sqlite3
from datetime import datetime
import config


def get_connection():
    """Get database connection"""
    return sqlite3.connect(config.DB_NAME)


def generate_transaction_report(start_date=None, end_date=None):
    """Generate transaction report"""
    conn = get_connection()
    c = conn.cursor()
    
    # Build query with date filters
    query = '''
        SELECT 
            t.id,
            t.date,
            t.transaction_type,
            t.quantity,
            t.notes,
            i.name as item_name,
            c.name as category,
            mu.unit_symbol,
            COALESCE(t.selling_price, 0.0) as value
        FROM transactions t
        LEFT JOIN inventory i ON t.item_id = i.id
        LEFT JOIN categories c ON i.category_id = c.id
        LEFT JOIN measurement_units mu ON i.measurement_unit_id = mu.id
    '''
    
    params = []
    if start_date:
        query += " WHERE t.date >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND t.date <= ?"
        params.append(end_date)
    
    query += " ORDER BY t.date DESC, t.created_at DESC"
    
    c.execute(query, params)
    transactions = c.fetchall()
    conn.close()
    
    return {
        'transactions': transactions,
        'total_transactions': len(transactions),
        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'filter_period': f"{start_date or 'All'} to {end_date or 'Present'}"
    }


def generate_sales_report(start_date=None, end_date=None):
    """Generate sales report"""
    conn = get_connection()
    c = conn.cursor()
    
    # Build query with date filters
    query = '''
        SELECT 
            i.name,
            SUM(t.quantity) as total_sold,
            SUM(t.quantity * COALESCE(t.selling_price, 0.0)) as total_revenue
        FROM transactions t
        LEFT JOIN inventory i ON t.item_id = i.id
        WHERE t.transaction_type = 'OUT'
    '''
    
    params = []
    if start_date:
        query += " AND t.date >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND t.date <= ?"
        params.append(end_date)
    
    query += " GROUP BY i.id, i.name ORDER BY total_revenue DESC"
    
    c.execute(query, params)
    sales_data = c.fetchall()
    conn.close()
    
    total_sales = sum(sale[2] for sale in sales_data) if sales_data else 0
    total_items_sold = sum(sale[1] for sale in sales_data) if sales_data else 0
    average_sale = total_sales / len(sales_data) if sales_data else 0
    
    return {
        'sales': sales_data,
        'total_sales': total_sales,
        'total_items_sold': total_items_sold,
        'average_sale': average_sale,
        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'filter_period': f"{start_date or 'All'} to {end_date or 'Present'}"
    }


def generate_inventory_report(start_date=None, end_date=None):
    """Generate inventory report"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT 
            i.*,
            c.name as category_name,
            mu.unit_symbol
        FROM inventory i
        LEFT JOIN categories c ON i.category_id = c.id
        LEFT JOIN measurement_units mu ON i.measurement_unit_id = mu.id
        ORDER BY i.name
    ''')
    
    items = c.fetchall()
    conn.close()
    
    # Calculate statistics
    total_items = len(items)
    total_value = sum(item[4] * item[3] for item in items)  # cost_price * quantity
    
    # Group by category
    categories = {}
    low_stock = []
    
    for item in items:
        category = item[7] or "Uncategorized"  # category_name
        if category not in categories:
            categories[category] = {'count': 0, 'value': 0}
        
        categories[category]['count'] += 1
        categories[category]['value'] += item[4] * item[3]  # cost_price * quantity
        
        # Check for low stock (less than 10)
        if item[3] < 10:  # quantity
            low_stock.append(item)
    
    return {
        'items': items,
        'total_items': total_items,
        'total_value': total_value,
        'categories': [(cat, data['count'], data['value']) for cat, data in categories.items()],
        'low_stock': low_stock,
        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'filter_period': f"{start_date or 'All'} to {end_date or 'Present'}"
    }


def generate_supplier_report(start_date=None, end_date=None):
    """Generate supplier report"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM suppliers ORDER BY name")
    suppliers = c.fetchall()
    conn.close()
    
    return {
        'suppliers': suppliers,
        'total_suppliers': len(suppliers),
        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'filter_period': f"{start_date or 'All'} to {end_date or 'Present'}"
    }
