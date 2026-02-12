import unittest
import os
import tempfile
import shutil
from database import models
import config


class TestDatabaseModels(unittest.TestCase):
    """Test database models functionality"""
    
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
    
    def test_add_item(self):
        """Test adding inventory items"""
        models.add_item("Test Item", "Test Category", 10, 25.50)
        items = models.view_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][1], "Test Item")
        self.assertEqual(items[0][2], "Test Category")
        self.assertEqual(items[0][3], 10)
        self.assertEqual(items[0][4], 25.50)
    
    def test_update_item(self):
        """Test updating inventory items"""
        # Add item first
        models.add_item("Original Name", "Category", 5, 10.0)
        items = models.view_items()
        item_id = items[0][0]
        
        # Update item
        models.update_item(item_id, name="Updated Name", quantity=15)
        updated_items = models.view_items()
        self.assertEqual(updated_items[0][1], "Updated Name")
        self.assertEqual(updated_items[0][3], 15)
    
    def test_delete_item(self):
        """Test deleting inventory items"""
        # Add item first
        models.add_item("To Delete", "Category", 5, 10.0)
        items = models.view_items()
        item_id = items[0][0]
        
        # Delete item
        models.delete_item(item_id)
        remaining_items = models.view_items()
        self.assertEqual(len(remaining_items), 0)
    
    def test_add_category(self):
        """Test adding categories"""
        models.add_category("Electronics", "Electronic devices")
        categories = models.view_categories()
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0][1], "Electronics")
        self.assertEqual(categories[0][2], "Electronic devices")
    
    def test_add_supplier(self):
        """Test adding suppliers"""
        models.add_supplier("Test Supplier", "John Doe", "123-456-7890", 
                           "test@supplier.com", "123 Main St")
        suppliers = models.view_suppliers()
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0][1], "Test Supplier")
        self.assertEqual(suppliers[0][2], "John Doe")
    
    def test_add_transaction(self):
        """Test adding transactions"""
        # Add item first for foreign key
        models.add_item("Test Item", "Category", 10, 25.0)
        items = models.view_items()
        item_id = items[0][0]
        
        # Add transaction
        models.add_transaction(item_id, "IN", 5, "2026-02-12", "Initial stock")
        transactions = models.view_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0][1], item_id)
        self.assertEqual(transactions[0][2], "IN")
        self.assertEqual(transactions[0][3], 5)


if __name__ == '__main__':
    unittest.main()
