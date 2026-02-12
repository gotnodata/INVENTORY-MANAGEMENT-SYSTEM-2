import unittest
from utils.validators import (
    validate_username, validate_password, validate_item_data,
    validate_quantity, validate_price
)


class TestValidators(unittest.TestCase):
    """Test input validation functions"""
    
    def test_validate_username(self):
        """Test username validation"""
        # Valid usernames
        self.assertTrue(validate_username("testuser")[0])
        self.assertTrue(validate_username("user123")[0])
        self.assertTrue(validate_username("user_name")[0])
        
        # Invalid usernames
        self.assertFalse(validate_username("")[0])
        self.assertFalse(validate_username("   ")[0])
        self.assertFalse(validate_username(None)[0])
    
    def test_validate_password(self):
        """Test password validation"""
        # Valid passwords (assuming MIN_PASSWORD_LENGTH = 4)
        self.assertTrue(validate_password("1234")[0])
        self.assertTrue(validate_password("password")[0])
        self.assertTrue(validate_password("pass123")[0])
        
        # Invalid passwords
        self.assertFalse(validate_password("")[0])
        self.assertFalse(validate_password("123")[0])  # Too short
        self.assertFalse(validate_password(None)[0])
    
    def test_validate_item_data(self):
        """Test item data validation"""
        # Valid item data
        self.assertTrue(validate_item_data("Test Item", "Electronics", "10", "25.50")[0])
        self.assertTrue(validate_item_data("Item", "Category", "5", "10.0")[0])
        
        # Invalid item data
        self.assertFalse(validate_item_data("", "Category", "10", "25.50")[0])
        self.assertFalse(validate_item_data("Item", "", "10", "25.50")[0])
        self.assertFalse(validate_item_data("Item", "Category", "abc", "25.50")[0])
        self.assertFalse(validate_item_data("Item", "Category", "10", "abc")[0])
    
    def test_validate_quantity(self):
        """Test quantity validation"""
        # Valid quantities
        self.assertTrue(validate_quantity("10")[0])
        self.assertTrue(validate_quantity("0")[0])
        self.assertTrue(validate_quantity("-5")[0])  # Negative allowed in validation
        
        # Invalid quantities
        self.assertFalse(validate_quantity("abc")[0])
        self.assertFalse(validate_quantity("10.5")[0])  # Not integer
        self.assertFalse(validate_quantity("")[0])
        self.assertFalse(validate_quantity(None)[0])
    
    def test_validate_price(self):
        """Test price validation"""
        # Valid prices
        self.assertTrue(validate_price("25.50")[0])
        self.assertTrue(validate_price("10")[0])
        self.assertTrue(validate_price("0")[0])
        self.assertTrue(validate_price("-5.25")[0])  # Negative allowed in validation
        
        # Invalid prices
        self.assertFalse(validate_price("abc")[0])
        self.assertFalse(validate_price("")[0])
        self.assertFalse(validate_price(None)[0])


if __name__ == '__main__':
    unittest.main()
