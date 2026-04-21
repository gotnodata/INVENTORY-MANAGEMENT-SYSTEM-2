"""Users database model and operations"""
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


def get_users():
    """Get all users"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = c.fetchall()
    conn.close()
    return users


def generate_user_activity_report(start_date=None, end_date=None):
    """Generate user activity report"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = c.fetchall()
    conn.close()
    
    return {
        'users': users,
        'total_users': len(users),
        'active_users': len([u for u in users if u[3] == 'admin']),  # role
        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'filter_period': f"{start_date or 'All'} to {end_date or 'Present'}"
    }
