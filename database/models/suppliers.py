"""Suppliers database model and operations"""
import sqlite3
import config


def get_connection():
    """Get database connection"""
    return sqlite3.connect(config.DB_NAME)


def add_supplier(name, contact=None, email=None, phone=None):
    """Add a new supplier"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO suppliers (name, contact, email, phone)
        VALUES (?, ?, ?)
    ''', (name, contact, email, phone))
    
    conn.commit()
    conn.close()


def get_suppliers():
    """Get all suppliers"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM suppliers ORDER BY name")
    suppliers = c.fetchall()
    conn.close()
    return suppliers


def update_supplier(supplier_id, name=None, contact=None, email=None, phone=None):
    """Update supplier"""
    conn = get_connection()
    c = conn.cursor()
    
    # Build dynamic update query
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = ?")
        values.append(name)
    
    if contact is not None:
        updates.append("contact = ?")
        values.append(contact)
    
    if email is not None:
        updates.append("email = ?")
        values.append(email)
    
    if phone is not None:
        updates.append("phone = ?")
        values.append(phone)
    
    if updates:
        values.append(supplier_id)
        query = f"UPDATE suppliers SET {', '.join(updates)} WHERE id = ?"
        c.execute(query, values)
        conn.commit()
    
    conn.close()


def delete_supplier(supplier_id):
    """Delete supplier"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
    conn.commit()
    conn.close()
