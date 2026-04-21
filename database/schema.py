"""Database table schema definitions"""
from database.connection import get_connection


def init_db():
    """Initialize the main inventory database table"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category_id INTEGER,
            quantity INTEGER NOT NULL DEFAULT 0,
            price REAL NOT NULL DEFAULT 0.0,
            measurement_unit_id INTEGER,
            cost_price REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (measurement_unit_id) REFERENCES measurement_units (id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS measurement_units (
            id INTEGER PRIMARY KEY,
            unit_name TEXT UNIQUE NOT NULL,
            unit_symbol TEXT UNIQUE NOT NULL
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
            id INTEGER PRIMARY KEY,
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
            id INTEGER PRIMARY KEY,
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
            id INTEGER PRIMARY KEY,
            item_id INTEGER,
            transaction_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            selling_price REAL DEFAULT 0.0,
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
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT NOT NULL
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
            id INTEGER PRIMARY KEY,
            unit_name TEXT UNIQUE NOT NULL,
            unit_symbol TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def init_default_measurement_units():
    """Initialize default measurement units"""
    default_units = [
        ('Pieces', 'pcs'),
        ('Kilograms', 'kgs'),
        ('Liters', 'L'),
        ('Meters', 'm'),
        ('Boxes', 'boxes'),
        ('Bottles', 'bottles'),
        ('Bags', 'bags'),
        ('Cartons', 'cartons')
    ]
    
    conn = get_connection()
    c = conn.cursor()
    for unit_name, unit_symbol in default_units:
        c.execute('INSERT OR IGNORE INTO measurement_units (unit_name, unit_symbol) VALUES (?, ?)',
                  (unit_name, unit_symbol))
    conn.commit()
    conn.close()


def create_profit_loss_table():
    """Create profit_loss_summary table for P&L tracking"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS profit_loss_summary (
            id INTEGER PRIMARY KEY,
            period_start TEXT NOT NULL,
            period_end TEXT NOT NULL,
            total_revenue REAL DEFAULT 0.0,
            total_cost REAL DEFAULT 0.0,
            gross_profit REAL DEFAULT 0.0,
            net_profit REAL DEFAULT 0.0,
            items_sold INTEGER DEFAULT 0,
            items_purchased INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()
