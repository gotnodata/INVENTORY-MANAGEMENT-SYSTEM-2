"""Inventory database model and operations"""
import sqlite3
import config


def get_connection():
    """Get database connection"""
    return sqlite3.connect(config.DB_NAME)


def add_item(name, category_id, quantity, cost_price):
    """Add a new inventory item"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO inventory (name, category, quantity, price)
        VALUES (?, ?, ?, ?)
    ''', (name, category_id, quantity, cost_price))
    
    conn.commit()
    conn.close()


def get_items():
    """Get all inventory items"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT i.*, c.name, mu.unit_name, mu.unit_symbol
        FROM inventory i
        LEFT JOIN categories c ON i.category_id = c.id
        LEFT JOIN measurement_units mu ON i.measurement_unit_id = mu.id
        ORDER BY i.name
    ''')
    
    items = c.fetchall()
    conn.close()
    return items


def get_item_by_id(item_id):
    """Get item by ID"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT i.*, c.name, mu.unit_name, mu.unit_symbol
        FROM inventory i
        LEFT JOIN categories c ON i.category_id = c.id
        LEFT JOIN measurement_units mu ON i.measurement_unit_id = mu.id
        WHERE i.id = ?
    ''', (item_id,))
    
    item = c.fetchone()
    conn.close()
    return item


def update_item(item_id, name=None, category_id=None, quantity=None, cost_price=None):
    """Update inventory item"""
    conn = get_connection()
    c = conn.cursor()
    
    # Build dynamic update query
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = ?")
        values.append(name)
    
    if category_id is not None:
        updates.append("category_id = ?")
        values.append(category_id)
    
    if quantity is not None:
        updates.append("quantity = ?")
        values.append(quantity)
    
    if cost_price is not None:
        updates.append("cost_price = ?")
        values.append(cost_price)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(item_id)
        
        query = f"UPDATE inventory SET {', '.join(updates)} WHERE id = ?"
        c.execute(query, values)
        conn.commit()
    
    conn.close()


def delete_item(item_id):
    """Delete inventory item"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def view_items():
    """Get all inventory items with category and unit info"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT * FROM inventory
        ORDER BY name
    ''')
    
    items = c.fetchall()
    conn.close()
    return items
