import hashlib
from datetime import datetime
from database import models


def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hash_value):
    """Verify a password against its hash"""
    return hash_password(password) == hash_value


def create_user(username, password, email=None, role='user'):
    """Create a new user account"""
    conn = models.get_connection()
    c = conn.cursor()
    
    # Check if user already exists
    c.execute('SELECT id FROM users WHERE username = ?', (username,))
    if c.fetchone():
        conn.close()
        return False
    
    # Create user
    password_hash = hash_password(password)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('INSERT INTO users (username, password_hash, email, role, created_at) VALUES (?, ?, ?, ?, ?)',
              (username, password_hash, email, role, created_at))
    conn.commit()
    conn.close()
    return True


def authenticate_user(username, password):
    """Authenticate a user and return user info if successful"""
    conn = models.get_connection()
    c = conn.cursor()
    c.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and verify_password(password, user[2]):
        return {'id': user[0], 'username': user[1], 'role': user[3]}
    return None


def get_all_users():
    """Get all users (for admin purposes)"""
    conn = models.get_connection()
    c = conn.cursor()
    c.execute('SELECT id, username, email, role, created_at FROM users')
    users = c.fetchall()
    conn.close()
    return users
