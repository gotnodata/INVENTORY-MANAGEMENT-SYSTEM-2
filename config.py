# Configuration and Constants for Inventory Management System.
# Controls the systems behavior.

# Database Configuration
DB_NAME = 'inventory.db'

# GUI Configuration
MAIN_WINDOW_TITLE = "Inventory Management System"
MAIN_WINDOW_GEOMETRY = "1200x700"
LOGIN_WINDOW_GEOMETRY = "400x300"
DIALOG_WINDOW_GEOMETRY = "400x350"

# UI Constants
DEFAULT_FONT_TITLE = ("Arial", 16, "bold")
DEFAULT_FONT_LABEL = ("Arial", 14, "bold")
DEFAULT_FONT_BODY = ("Arial", 10)
DEFAULT_FONT_SMALL = ("Arial", 9)

# TreeView Column Widths
COLUMN_WIDTH_ID = 50
COLUMN_WIDTH_NAME = 120
COLUMN_WIDTH_STANDARD = 100
COLUMN_WIDTH_WIDE = 150

# Password Constraints
MIN_PASSWORD_LENGTH = 4

# User Roles
ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

# Transaction Types
TRANSACTION_TYPE_IN = 'IN'
TRANSACTION_TYPE_OUT = 'OUT'
