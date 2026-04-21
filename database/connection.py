"""Database connection and schema management module"""
import sqlite3
from datetime import datetime
import config


def get_connection():
    """Get a database connection"""
    return sqlite3.connect(config.DB_NAME)


def update_database_schema():
    """Update existing database schema to add new columns"""
    conn = get_connection()
    c = conn.cursor()
    
    # Check if measurement_unit_id column exists in inventory table
    c.execute("PRAGMA table_info(inventory)")
    columns = [column[1] for column in c.fetchall()]
    
    # Add category_id column if it doesn't exist
    if 'category_id' not in columns:
        c.execute('ALTER TABLE inventory ADD COLUMN category_id INTEGER')
    
    # Add measurement_unit_id column if it doesn't exist
    if 'measurement_unit_id' not in columns:
        c.execute('ALTER TABLE inventory ADD COLUMN measurement_unit_id INTEGER')
    
    # Add cost_price column if it doesn't exist
    if 'cost_price' not in columns:
        c.execute('ALTER TABLE inventory ADD COLUMN cost_price REAL DEFAULT 0.0')
    
    # Check if transactions table needs selling_price column
    c.execute("PRAGMA table_info(transactions)")
    trans_columns = [column[1] for column in c.fetchall()]
    
    if 'selling_price' not in trans_columns:
        c.execute('ALTER TABLE transactions ADD COLUMN selling_price REAL DEFAULT 0.0')
    
    # Check if measurement_units table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='measurement_units'")
    if not c.fetchone():
        from database.schema import create_measurement_units_table, init_default_measurement_units
        create_measurement_units_table()
        init_default_measurement_units()
    
    # Check if profit_loss_summary table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='profit_loss_summary'")
    if not c.fetchone():
        from database.schema import create_profit_loss_table
        create_profit_loss_table()
    
    conn.commit()
    conn.close()


def get_next_available_id(table_name):
    """Get next available ID for any table, reusing deleted IDs"""
    conn = get_connection()
    c = conn.cursor()
    
    # Get all existing IDs from the specified table
    c.execute(f'SELECT id FROM {table_name} ORDER BY id')
    existing_ids = [row[0] for row in c.fetchall()]
    conn.close()
    
    # Find first missing ID starting from 1
    next_id = 1
    while next_id in existing_ids:
        next_id += 1
    
    return next_id
