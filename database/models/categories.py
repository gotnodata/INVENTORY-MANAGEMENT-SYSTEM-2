"""Categories database model and operations"""
import sqlite3
import config


def get_connection():
    """Get database connection"""
    return sqlite3.connect(config.DB_NAME)


def add_category(name, description=None):
    """Add a new category"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    ''', (name, description))
    
    conn.commit()
    conn.close()


def get_categories():
    """Get all categories"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM categories ORDER BY name")
    categories = c.fetchall()
    conn.close()
    return categories


def update_category(category_id, name=None, description=None):
    """Update category"""
    conn = get_connection()
    c = conn.cursor()
    
    # Build dynamic update query
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = ?")
        values.append(name)
    
    if description is not None:
        updates.append("description = ?")
        values.append(description)
    
    if updates:
        values.append(category_id)
        query = f"UPDATE categories SET {', '.join(updates)} WHERE id = ?"
        c.execute(query, values)
        conn.commit()
    
    conn.close()


def delete_category(category_id):
    """Delete category"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()
