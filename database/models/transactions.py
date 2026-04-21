"""Transactions database model and operations"""
import sqlite3
import config


def get_connection():
    """Get database connection"""
    return sqlite3.connect(config.DB_NAME)


def add_transaction(item_id, transaction_type, quantity, date, notes=None, selling_price=None):
    """Add a new transaction"""
    conn = get_connection()
    c = conn.cursor()
    
    # Get current item quantity
    c.execute("SELECT quantity FROM inventory WHERE id = ?", (item_id,))
    item = c.fetchone()
    
    if not item:
        conn.close()
        return False, "Item not found"
    
    current_quantity = item[0]
    
    # Update inventory based on transaction type
    if transaction_type == config.TRANSACTION_TYPE_OUT:
        if quantity > current_quantity:
            conn.close()
            return False, "Insufficient inventory"
        new_quantity = current_quantity - quantity
    else:  # IN transaction
        new_quantity = current_quantity + quantity
    
    # Add transaction
    c.execute('''
        INSERT INTO transactions (item_id, transaction_type, quantity, date, notes, selling_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (item_id, transaction_type, quantity, date, notes, selling_price))
    
    # Update inventory quantity
    c.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (new_quantity, item_id))
    
    conn.commit()
    conn.close()
    return True, "Transaction added successfully"


def get_transactions():
    """Get all transactions"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT t.*, i.name as item_name
        FROM transactions t
        LEFT JOIN inventory i ON t.item_id = i.id
        ORDER BY t.date DESC
        LIMIT 100
    ''')
    
    transactions = c.fetchall()
    conn.close()
    return transactions
