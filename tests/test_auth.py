import unittest
import os
import tempfile
from auth import auth
from database import models
import config


class TestAuthentication(unittest.TestCase):
    """Test authentication functionality"""
    
    def setUp(self):
        """Set up test database"""
        # Create temporary database for testing
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        # Override config for testing
        self.original_db = config.DB_NAME
        config.DB_NAME = self.test_db.name
        
        # Initialize test database
        models.init_db()
        models.create_categories_table()
        models.create_suppliers_table()
        models.create_transactions_table()
        models.create_users_table()
    
    def tearDown(self):
        """Clean up test database"""
        # Restore original config
        config.DB_NAME = self.original_db
        
        # Remove test database
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_create_user(self):
        """Test user creation"""
        result = auth.create_user("testuser", "password123", "test@example.com", "user")
        self.assertTrue(result)
        
        # Verify user was created
        users = auth.get_all_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], "testuser")
        self.assertEqual(users[0][2], "test@example.com")
        self.assertEqual(users[0][3], "user")
    
    def test_create_duplicate_user(self):
        """Test creating duplicate user"""
        # Create first user
        auth.create_user("testuser", "password123", "test@example.com", "user")
        
        # Try to create duplicate
        result = auth.create_user("testuser", "differentpass", "test2@example.com", "admin")
        self.assertFalse(result)
    
    def test_authenticate_user(self):
        """Test user authentication"""
        # Create user first
        auth.create_user("testuser", "password123", "test@example.com", "user")
        
        # Test correct authentication
        user = auth.authenticate_user("testuser", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['role'], "user")
        
        # Test incorrect password
        user = auth.authenticate_user("testuser", "wrongpass")
        self.assertIsNone(user)
        
        # Test non-existent user
        user = auth.authenticate_user("nonexistent", "password123")
        self.assertIsNone(user)
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "testpassword"
        hash1 = auth.hash_password(password)
        hash2 = auth.hash_password(password)
        
        # Same password should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Hash should be different from password
        self.assertNotEqual(hash1, password)
    
    def test_verify_password(self):
        """Test password verification"""
        password = "testpassword"
        hash_value = auth.hash_password(password)
        
        # Correct password should verify
        self.assertTrue(auth.verify_password(password, hash_value))
        
        # Incorrect password should not verify
        self.assertFalse(auth.verify_password("wrongpass", hash_value))
    
    def test_get_all_users(self):
        """Test retrieving all users"""
        # Create multiple users
        auth.create_user("user1", "pass1", "user1@example.com", "user")
        auth.create_user("admin1", "pass2", "admin@example.com", "admin")
        
        users = auth.get_all_users()
        self.assertEqual(len(users), 2)
        
        # Check user data structure
        for user in users:
            self.assertEqual(len(user), 5)  # id, username, email, role, created_at
            self.assertIsInstance(user[0], int)  # id
            self.assertIsInstance(user[1], str)  # username
            self.assertIsInstance(user[3], str)  # role


if __name__ == '__main__':
    unittest.main()
