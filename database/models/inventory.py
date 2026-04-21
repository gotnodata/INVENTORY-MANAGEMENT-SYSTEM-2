"""Inventory database model and operations"""
import sqlite3
import config

# region agent log
import os as _agent_os
_DEBUG_LOG_PATH = _agent_os.path.join(_agent_os.path.dirname(_agent_os.path.abspath(__file__)), "..", "..", "debug-31c49c.log")

def _agent_log(hypothesisId: str, location: str, message: str, data: dict | None = None, runId: str = "pre-fix"):
    try:
        import json, time
        payload = {
            "sessionId": "31c49c",
            "runId": runId,
            "hypothesisId": hypothesisId,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass
# endregion


def get_connection():
    """Get database connection"""
    return sqlite3.connect(config.DB_NAME)


def add_item(name, category_id, quantity, cost_price):
    """Add a new inventory item"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO inventory (name, category_id, quantity, price, cost_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, category_id, quantity, 0.0, cost_price))
    
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
        SELECT
            i.id,
            i.name,
            i.category_id,
            i.quantity,
            i.price,
            i.measurement_unit_id,
            c.name AS category_name,
            mu.unit_name,
            mu.unit_symbol,
            i.cost_price
        FROM inventory i
        LEFT JOIN categories c ON i.category_id = c.id
        LEFT JOIN measurement_units mu ON i.measurement_unit_id = mu.id
        ORDER BY i.name
    ''')
    
    items = c.fetchall()
    _agent_log(
        "H-view-items",
        "database/models/inventory.py:view_items",
        "Fetched inventory items",
        {"rows": len(items), "cols_first_row": (len(items[0]) if items else 0)},
    )
    conn.close()
    return items
