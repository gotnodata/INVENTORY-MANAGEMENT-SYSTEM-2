"""
Unit tests for configuration module
"""
import unittest
import config


class TestConfigConstants(unittest.TestCase):
    """Test configuration constants"""
    
    def test_database_config_exists(self):
        """Test database configuration"""
        self.assertIsNotNone(config.DB_NAME)
        self.assertEqual(config.DB_NAME, 'inventory.db')
    
    def test_window_geometry_valid(self):
        """Test window geometry is valid"""
        # Should be in format "WIDTHxHEIGHT"
        self.assertIn('x', config.MAIN_WINDOW_GEOMETRY)
        self.assertIn('x', config.LOGIN_WINDOW_GEOMETRY)
    
    def test_user_roles_defined(self):
        """Test user roles are defined"""
        self.assertTrue(hasattr(config, 'ROLE_ADMIN'))
        self.assertTrue(hasattr(config, 'ROLE_USER'))
        
        self.assertEqual(config.ROLE_ADMIN, 'admin')
        self.assertEqual(config.ROLE_USER, 'user')
    
    def test_password_constraints(self):
        """Test password constraints"""
        self.assertIsNotNone(config.MIN_PASSWORD_LENGTH)
        self.assertGreaterEqual(config.MIN_PASSWORD_LENGTH, 4)
    
    def test_transaction_types_defined(self):
        """Test transaction types are defined"""
        self.assertTrue(hasattr(config, 'TRANSACTION_TYPE_IN'))
        self.assertTrue(hasattr(config, 'TRANSACTION_TYPE_OUT'))
        
        self.assertEqual(config.TRANSACTION_TYPE_IN, 'IN')
        self.assertEqual(config.TRANSACTION_TYPE_OUT, 'OUT')
    
    def test_color_constants_defined(self):
        """Test color constants are defined"""
        colors = [
            'COLOR_PRIMARY', 'COLOR_SUCCESS', 'COLOR_WARNING',
            'COLOR_DANGER', 'COLOR_INFO', 'COLOR_DARK', 'COLOR_LIGHT'
        ]
        
        for color in colors:
            self.assertTrue(hasattr(config, color), f"Missing {color}")
            # Colors should be hex strings starting with #
            value = getattr(config, color)
            self.assertTrue(value.startswith('#'), f"{color} should be hex color")
    
    def test_font_configuration(self):
        """Test font configuration"""
        fonts = [
            'DEFAULT_FONT_TITLE', 'DEFAULT_FONT_LABEL',
            'DEFAULT_FONT_BODY'
        ]
        
        for font in fonts:
            self.assertTrue(hasattr(config, font), f"Missing {font}")
            font_value = getattr(config, font)
            self.assertIsInstance(font_value, tuple)
            self.assertGreaterEqual(len(font_value), 2)  # Font name and size
    
    def test_ui_constants(self):
        """Test UI constants"""
        self.assertIsNotNone(config.ENTRY_FIELD_WIDTH)
        self.assertIsNotNone(config.DIALOG_PADDING)
        
        self.assertGreater(config.ENTRY_FIELD_WIDTH, 0)
        self.assertGreater(config.DIALOG_PADDING, 0)
    
    def test_currency_symbol(self):
        """Test currency symbol is configured"""
        self.assertIsNotNone(config.CURRENCY_SYMBOL)
        self.assertEqual(config.CURRENCY_SYMBOL, 'KES')
    
    def test_window_title(self):
        """Test application title"""
        self.assertIsNotNone(config.MAIN_WINDOW_TITLE)
        self.assertEqual(config.MAIN_WINDOW_TITLE, "Inventory Management System")


if __name__ == '__main__':
    unittest.main()
