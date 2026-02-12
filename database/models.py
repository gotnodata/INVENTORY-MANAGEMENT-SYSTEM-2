import sqlite3
from datetime import datetime
import config


def get_connection():
    """Get a database connection"""
    return sqlite3.connect(config.DB_NAME)


def init_db():
    """Initialize the main inventory database table"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def create_categories_table():
    """Create a categories table to manage product categories"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()


def create_suppliers_table():
    """Create a suppliers table to track supplier information"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()


def create_transactions_table():
    """Create a transactions table to log inventory movements"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            transaction_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (item_id) REFERENCES inventory (id)
        )
    ''')
    conn.commit()
    conn.close()


def create_users_table():
    """Create a users table for authentication"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Inventory Item Operations
def add_item(name, category, quantity, price):
    """Add a new item to inventory"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO inventory (name, category, quantity, price) VALUES (?, ?, ?, ?)',
              (name, category, quantity, price))
    conn.commit()
    conn.close()


def view_items():
    """Get all items from inventory"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()
    conn.close()
    return items


def get_all_items():
    """Get all items from inventory"""
    return view_items()


def update_item(item_id, name=None, category=None, quantity=None, price=None):
    """Update an inventory item"""
    conn = get_connection()
    c = conn.cursor()
    fields = []
    values = []
    
    if name is not None:
        fields.append('name = ?')
        values.append(name)
    if category is not None:
        fields.append('category = ?')
        values.append(category)
    if quantity is not None:
        fields.append('quantity = ?')
        values.append(quantity)
    if price is not None:
        fields.append('price = ?')
        values.append(price)
    
    if not fields:
        conn.close()
        return
        
    values.append(item_id)
    sql = f'UPDATE inventory SET {", ".join(fields)} WHERE id = ?'
    c.execute(sql, values)
    conn.commit()
    conn.close()


def delete_item(item_id):
    """Delete an item from inventory"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()


# Category Operations
def add_category(name, description=None):
    """Add a new category"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()


def view_categories():
    """Get all categories"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM categories')
    categories = c.fetchall()
    conn.close()
    return categories


def update_category(category_id, name=None, description=None):
    """Update a category"""
    conn = get_connection()
    c = conn.cursor()
    fields = []
    values = []
    
    if name is not None:
        fields.append('name = ?')
        values.append(name)
    if description is not None:
        fields.append('description = ?')
        values.append(description)
    
    if not fields:
        conn.close()
        return
        
    values.append(category_id)
    sql = f'UPDATE categories SET {", ".join(fields)} WHERE id = ?'
    c.execute(sql, values)
    conn.commit()
    conn.close()


def delete_category(category_id):
    """Delete a category"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()


# Supplier Operations
def add_supplier(name, contact_person=None, phone=None, email=None, address=None):
    """Add a new supplier"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO suppliers (name, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?)',
              (name, contact_person, phone, email, address))
    conn.commit()
    conn.close()


def view_suppliers():
    """Get all suppliers"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM suppliers')
    suppliers = c.fetchall()
    conn.close()
    return suppliers


def update_supplier(supplier_id, name=None, contact_person=None, phone=None, email=None, address=None):
    """Update a supplier"""
    conn = get_connection()
    c = conn.cursor()
    fields = []
    values = []
    
    if name is not None:
        fields.append('name = ?')
        values.append(name)
    if contact_person is not None:
        fields.append('contact_person = ?')
        values.append(contact_person)
    if phone is not None:
        fields.append('phone = ?')
        values.append(phone)
    if email is not None:
        fields.append('email = ?')
        values.append(email)
    if address is not None:
        fields.append('address = ?')
        values.append(address)
    
    if not fields:
        conn.close()
        return
        
    values.append(supplier_id)
    sql = f'UPDATE suppliers SET {", ".join(fields)} WHERE id = ?'
    c.execute(sql, values)
    conn.commit()
    conn.close()


def delete_supplier(supplier_id):
    """Delete a supplier"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM suppliers WHERE id = ?', (supplier_id,))
    conn.commit()
    conn.close()


# Transaction Operations
def add_transaction(item_id, transaction_type, quantity, date, notes=None):
    """Add a new transaction"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO transactions (item_id, transaction_type, quantity, date, notes) VALUES (?, ?, ?, ?, ?)',
              (item_id, transaction_type, quantity, date, notes))
    conn.commit()
    conn.close()


def view_transactions():
    """Get all transactions"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT t.*, i.name as item_name 
        FROM transactions t 
        LEFT JOIN inventory i ON t.item_id = i.id 
        ORDER BY t.date DESC
    ''')
    transactions = c.fetchall()
    conn.close()
    return transactions


def view_transactions_by_item(item_id):
    """Get transactions for a specific item"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT t.*, i.name as item_name 
        FROM transactions t 
        LEFT JOIN inventory i ON t.item_id = i.id 
        WHERE t.item_id = ?
        ORDER BY t.date DESC
    ''', (item_id,))
    transactions = c.fetchall()
    conn.close()
    return transactions


def clear_all_data():
    """Clear all data from all tables while preserving table structure"""
    conn = get_connection()
    c = conn.cursor()
    
    # Clear all tables in order to respect foreign key constraints
    tables = [
        'transactions',  # Clear transactions first (depends on inventory)
        'inventory',     # Clear inventory
        'categories',    # Clear categories
        'suppliers',     # Clear suppliers
        'users'          # Clear users last
    ]
    
    for table in tables:
        c.execute(f'DELETE FROM {table}')
    
    conn.commit()
    conn.close()
