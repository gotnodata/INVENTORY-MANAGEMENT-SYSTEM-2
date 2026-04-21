"""Database schema definitions and initialization"""
import sqlite3
import sys
import os
from datetime import datetime

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import config


def get_connection():
    """Get database connection"""
    return sqlite3.connect(config.DB_NAME)


def create_categories_table():
    """Create categories table"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def create_suppliers_table():
    """Create suppliers table"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def create_transactions_table():
    """Create transactions table"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL CHECK (transaction_type IN ('IN', 'OUT')),
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            selling_price REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES inventory (id)
        )
    ''')
    
    conn.commit()
    conn.close()


def create_users_table():
    """Create users table"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def create_measurement_units_table():
    """Create measurement units table"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS measurement_units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL UNIQUE,
            unit_symbol TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def init_db():
    """Initialize all database tables"""
    conn = get_connection()
    c = conn.cursor()
    
    # Create inventory table
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            quantity INTEGER DEFAULT 0,
            price REAL DEFAULT 0.0,
            cost_price REAL DEFAULT 0.0,
            measurement_unit_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (measurement_unit_id) REFERENCES measurement_units (id)
        )
    ''')
    
    # Create categories table
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create suppliers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL CHECK (transaction_type IN ('IN', 'OUT')),
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            selling_price REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES inventory (id)
        )
    ''')
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create measurement_units table
    c.execute('''
        CREATE TABLE IF NOT EXISTS measurement_units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL UNIQUE,
            unit_symbol TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def init_default_measurement_units():
    """Initialize default measurement units"""
    conn = get_connection()
    c = conn.cursor()
    
    # Check if units already exist
    c.execute("SELECT COUNT(*) FROM measurement_units")
    if c.fetchone()[0] > 0:
        conn.close()
        return
    
    # Insert default units
    default_units = [
        ('Pieces', 'pcs'),
        ('Kilograms', 'kg'),
        ('Liters', 'L'),
        ('Meters', 'm'),
        ('Boxes', 'box'),
        ('Bottles', 'btl'),
        ('Pairs', 'pairs'),
        ('Sets', 'sets')
    ]
    
    c.executemany('''
        INSERT INTO measurement_units (unit_name, unit_symbol) 
        VALUES (?, ?)
    ''', default_units)
    
    conn.commit()
    conn.close()


def update_database_schema():
    """Update existing database schema"""
    conn = get_connection()
    c = conn.cursor()
    
    # Add cost_price column if it doesn't exist
    try:
        c.execute("ALTER TABLE inventory ADD COLUMN cost_price REAL DEFAULT 0.0")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add measurement_unit_id column if it doesn't exist
    try:
        c.execute("ALTER TABLE inventory ADD COLUMN measurement_unit_id INTEGER")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add selling_price column to transactions if it doesn't exist
    try:
        c.execute("ALTER TABLE transactions ADD COLUMN selling_price REAL DEFAULT 0.0")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.close()
