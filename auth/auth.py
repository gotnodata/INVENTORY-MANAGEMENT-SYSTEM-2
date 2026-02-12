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


def delete_user(user_id):
    """Delete a user account"""
    conn = models.get_connection()
    c = conn.cursor()
    
    # Prevent deletion of the last admin user
    c.execute('SELECT COUNT(*) FROM users WHERE role = ?', (config.ROLE_ADMIN,))
    admin_count = c.fetchone()[0]
    
    c.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user_role = c.fetchone()
    
    if user_role and user_role[0] == config.ROLE_ADMIN and admin_count <= 1:
        conn.close()
        return False, "Cannot delete the last admin user!"
    
    try:
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True, "User deleted successfully!"
    except Exception as e:
        conn.close()
        return False, f"Failed to delete user: {str(e)}"


def get_all_users():
    """Get all users (for admin purposes)"""
    conn = models.get_connection()
    c = conn.cursor()
    c.execute('SELECT id, username, email, role, created_at FROM users')
    users = c.fetchall()
    conn.close()
    return users
