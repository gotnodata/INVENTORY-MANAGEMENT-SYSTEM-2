Inventory Management System

A comprehensive supermarket inventory management system built with Python and SQLite, featuring both console and graphical user interfaces with secure user authentication. 

## 🚀 Features

### Core Functionality
- **Inventory Management**: Add, view, update, and delete inventory items
- **Category Management**: Organize products into categories with descriptions
- **Supplier Management**: Track supplier information and contact details
- **Transaction Tracking**: Log stock movements (IN/OUT) with dates and notes
- **Search & Filter**: Find items quickly by name or category
- **Data Persistence**: SQLite database for reliable data storage

### 🔐 Authentication System
- **Secure Login**: Password-based authentication with SHA-256 hashing
- **Role-Based Access Control**: Admin and regular user roles
- **User Management**: Admins can create and manage user accounts
- **Session Management**: Secure login/logout functionality
- **First-Time Setup**: Automatic admin account creation on first run

### 🧪 Testing Suite
- **Comprehensive Tests**: 17 test cases covering all major functionality
- **Unit Testing**: Isolated tests for database, authentication, and validation
- **Automated Testing**: One-command test execution
- **Test Coverage**: Database operations, user authentication, input validation
- **CI/CD Ready**: Suitable for continuous integration pipelines

### User Interfaces
- **Graphical Interface (GUI)**: Modern tabbed interface with full authentication
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux
- **Responsive Design**: Clean, organized layout with status bar and menu system
- **Admin Features**: Database management and user administration tools

## 📋 System Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- SQLite3 (included with Python)

## 🛠️ Installation

1. **Clone/Download the project**
   ```bash
   cd "INVENTORY MANAGEMENT SYSTEM 2"
   ```

2. **Verify Python installation**
   ```bash
   python --version  # Requires Python 3.7 or higher
   ```

3. **No external packages required** - Uses only Python standard library
   - `tkinter` (included with Python)
   - `sqlite3` (included with Python)
   - `hashlib` (included with Python)

## 🎯 Quick Start

**Start the application:**
```bash
python main.py
```

**On first run:**
1. A setup dialog will prompt you to create the first admin user
2. Enter admin username, password, email (optional), and role
3. Login with your credentials
4. Full GUI interface will launch

The `inventory.db` database file is created automatically on first run.

## 📁 Project Structure

```
├── main.py ............................ Entry point
├── config.py .......................... Constants and configuration
├── database/
│   ├── __init__.py
│   └── models.py ...................... All database operations
├── auth/
│   ├── __init__.py
│   └── auth.py ........................ Authentication logic
├── ui/
│   ├── __init__.py
│   ├── login.py ....................... Login window
│   ├── windows.py ..................... Main application window
│   └── dialogs.py ..................... Dialog windows
├── utils/
│   ├── __init__.py
│   └── validators.py .................. Input validation
├── tests/
│   ├── test_models.py ................ Database operations tests
│   ├── test_auth.py ................. Authentication tests
│   ├── test_validators.py .......... Validation tests
│   ├── run_all_tests.py ............ Test runner script
│   └── README.md ................. Testing documentation
├── requirements-dev.txt .............. Development dependencies
├── inventory.db ....................... SQLite database (auto-created)
└── README.md
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `config.py` | Centralized configuration, constants, UI settings |
| `database/models.py` | Database operations (CRUD for all entities) |
| `auth/auth.py` | User authentication, password hashing, user management |
| `ui/login.py` | Login window interface |
| `ui/windows.py` | Main application window and tab management |
| `ui/dialogs.py` | Modal dialogs (user management, etc.) |
| `utils/validators.py` | Input validation for all forms |
| `tests/` | Comprehensive test suite for all modules |

### User Roles

#### Admin Users
- Full access to all inventory features
- **User Management**: Create, view, and manage user accounts
- **System Administration**: Complete control over system including database operations
- **GUI Access**: Additional "Users" tab and "Database" menu options
- **Data Management**: Ability to clear all database data with confirmation

#### Regular Users
- Standard inventory management features
- Can add, update, and view inventory items
- Can manage categories, suppliers, and transactions
- **Limited Access**: Cannot manage user accounts or access database administration

## 📊 Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username (required)
- `password_hash` - SHA-256 hashed password (required)
- `email` - User email address (optional)
- `role` - User role ('user' or 'admin', default: 'user')
- `created_at` - Account creation timestamp

### Inventory Table
- `id` - Primary key
- `name` - Product name (required)
- `category` - Product category
- `quantity` - Stock quantity (required)
- `price` - Unit price (required)

### Categories Table
- `id` - Primary key
- `name` - Category name (unique, required)
- `description` - Category description

### Suppliers Table
- `id` - Primary key
- `name` - Supplier name (required)
- `contact_person` - Contact person
- `phone` - Phone number
- `email` - Email address
- `address` - Physical address

### Transactions Table
- `id` - Primary key
- `item_id` - Foreign key to inventory
- `transaction_type` - 'IN' or 'OUT'
- `quantity` - Transaction quantity
- `date` - Transaction date
- `notes` - Optional notes

## 🖥️ GUI Features

### Login Window
- **Secure Authentication**: Username and password login
- **First-Time Setup**: Automatic admin account creation
- **Error Handling**: Clear error messages for invalid credentials

### Main Interface
- **Tabbed Layout**: Organized sections for different management areas
- **Status Bar**: Shows current logged-in user and role
- **Menu Bar**: File, Users (admin only), and Help menus
- **Responsive Design**: Clean, modern interface

### Inventory Tab
- Add new items with name, category, quantity, and price
- Update existing items by double-clicking rows
- Delete items with confirmation
- Search functionality to filter items
- Category dropdown populated from database

### Categories Tab
- Create and manage product categories
- Add descriptions for better organization
- Edit categories with double-click
- Delete categories with confirmation

### Suppliers Tab
- Comprehensive supplier information management
- Contact details tracking
- Full CRUD operations
- Address and contact person fields

### Transactions Tab
- Track stock movements
- IN/OUT transaction types
- Date tracking with current date default
- Item selection dropdown
- Transaction history with item names

### Users Tab (Admin Only)
- **User Management**: Add, view, and manage user accounts
- **Role Assignment**: Set users as 'user' or 'admin'
- **User Information**: View username, email, role, and creation date
- **Account Creation**: Dialog for adding new users with validation

## 💻 Console Interface (Legacy)

The old console interface from the original version is no longer the primary interface. The system now focuses on the modern GUI application. However, the core functionality remains:

- User authentication
- Inventory management
- Category and supplier management
- Transaction tracking
- Role-based user management

For development and testing of individual modules:
```python
# Import modules directly
from database import models
from auth import auth
from utils import validators

# Test database operations
models.add_item("Test Item", "Test Category", 10, 9.99)
items = models.view_items()
```

## 🔧 Technical Architecture

### Architecture Pattern
The system follows a **modular, layered architecture** for better maintainability:

**Layers:**
1. **Configuration Layer** (`config.py`) - All constants and settings
2. **Data Layer** (`database/models.py`) - Database operations
3. **Authentication Layer** (`auth/auth.py`) - User authentication
4. **Business Logic** - Integrated with data layer
5. **Presentation Layer** (`ui/`) - GUI components
6. **Utilities** (`utils/`) - Helper functions

### Technology Stack
- **Language**: Python 3.7+
- **GUI Framework**: tkinter
- **Database**: SQLite
- **Security**: SHA-256 password hashing
- **Architecture**: Modular with separation of concerns

### Design Principles
- ✅ **Single Responsibility** - Each module has one clear purpose
- ✅ **DRY (Don't Repeat Yourself)** - Code reusability
- ✅ **Separation of Concerns** - UI, data, and auth are separate
- ✅ **Testability** - Modules can be tested independently
- ✅ **Maintainability** - Easy to find and modify code
- ✅ **Scalability** - Easy to add new features

### Key Files & Their Roles
- `main.py` - Application entry point (35 lines)
- `config.py` - Configuration and constants (40 lines)
- `database/models.py` - All database operations (280 lines)
- `auth/auth.py` - Authentication and user management (50 lines)
- `ui/login.py` - Login window (65 lines)
- `ui/windows.py` - Main application window (680 lines)
- `ui/dialogs.py` - Dialog windows (50 lines)
- `utils/validators.py` - Input validation (45 lines)
- `inventory.db` - SQLite database (auto-created on first run)

## 🧪 Testing

### Running Tests
Execute the complete test suite with a single command:
```bash
python tests/run_all_tests.py
```

### Test Coverage
The test suite includes 17 comprehensive test cases:

**Database Tests (`test_models.py`)**
- ✅ CRUD operations for inventory items
- ✅ Category and supplier management
- ✅ Transaction logging with foreign key relationships
- ✅ Data integrity and constraints

**Authentication Tests (`test_auth.py`)**
- ✅ User creation and validation
- ✅ Password hashing and verification
- ✅ User authentication and session management
- ✅ Duplicate user prevention

**Validation Tests (`test_validators.py`)**
- ✅ Input validation for all forms
- ✅ Data type validation
- ✅ Required field validation
- ✅ Error handling for invalid inputs

### Running Individual Tests
```bash
# Test specific modules
python -m unittest tests.test_models
python -m unittest tests.test_auth
python -m unittest tests.test_validators

# Test specific methods
python -m unittest tests.test_models.TestDatabaseModels.test_add_item
```

### Test Features
- **Isolated Testing**: Uses temporary databases, won't affect production data
- **Comprehensive Coverage**: Tests success, failure, and edge cases
- **CI/CD Ready**: Suitable for automated testing pipelines
- **Fast Execution**: Optimized for quick development feedback

## 📝 Usage Examples

### Starting the Application
```bash
python main.py
```

This will:
1. Initialize the database with all required tables
2. Prompt for admin creation on first run
3. Display the login window
4. Launch the main application after successful login

### Importing Modules (Advanced Usage)

**Add an item to inventory:**
```python
from database import models
models.add_item("Laptop", "Electronics", 5, 999.99)
```

**Authenticate a user:**
```python
from auth import auth
user = auth.authenticate_user("admin", "password123")
if user:
    print(f"Logged in as: {user['username']}")
```

**Create a new user (admin only):**
```python
from auth import auth
success = auth.create_user("newuser", "password123", "user@example.com", "user")
if success:
    print("User created successfully!")
```

**Get all items:**
```python
from database import models
items = models.view_items()
for item in items:
    print(f"{item[1]} - Qty: {item[3]}, Price: ${item[4]}")
```

### Adding an Item (GUI)
1. Launch the application: `python main.py`
2. Login with your credentials
3. Navigate to the **Inventory** tab
4. Fill in the form fields (name, category, quantity, price)
5. Click "Add Item"

### Managing Users (Admin Only - GUI)
1. Login as admin
2. Click **Users** menu → "Add User"
3. Fill in username, password, email, and role
4. Click "Create User"

### Searching Items (GUI)
1. In the **Inventory** tab, enter search term in the search box
2. Search by item name or category
3. Click "Search" or "Refresh" to reset

### Managing Suppliers (GUI)
1. Navigate to the **Suppliers** tab
2. Add supplier information or update existing suppliers
3. Double-click a row to populate the form for editing

## .gitignore Recommendations

When version controlling this project, add the following to `.gitignore`:

```
# Database file (created automatically)
inventory.db

# Python cache
__pycache__/
*.pyc
*.pyo
*.egg-info/
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# Virtual environments
venv/
env/
```

## 🔄 Module Integration

The modular architecture allows for seamless integration:

```python
# Example: Complete workflow
from database import models
from auth import auth

# Create a user
auth.create_user("john", "pass123", "john@example.com", "user")

# Authenticate
user = auth.authenticate_user("john", "pass123")

# If authenticated, add inventory items
if user:
    models.add_item("Widget A", "Hardware", 50, 29.99)
    models.add_category("Hardware", "Hardware products")
```

## 🐛 Troubleshooting

### Common Issues

**Application won't start:**
- Check Python version: `python --version` (requires 3.7+)
- Ensure you're in the correct directory
- Make sure tkinter is available: `python -c "import tkinter"` (usually included)

**GUI won't display:**
- Linux: Install tkinter: `sudo apt-get install python3-tk`
- macOS: Should be included with Python; try reinstalling Python
- Windows: Check if tkinter is included in Python installation

**Login issues:**
- Ensure you created an admin user on first run
- Username and password are case-sensitive
- Check that the database file (`inventory.db`) exists

**Database errors:**
- Ensure write permissions in the project directory
- Delete `inventory.db` to start fresh (will create new on next run)
- Check if database file is not locked by another process

**Import errors:**
- Verify all `.py` files and folders are present
- Check that `__init__.py` files exist in all package directories
- Ensure you're running from the project root directory

**Port or permission issues:**
- Run with administrator/sudo if you encounter permission errors
- Check that the project directory is not read-only

### Testing Modules Independently

Test individual modules without starting the GUI:

```bash
# Test database initialization
python -c "from database import models; models.init_db(); print('✓ DB initialized')"

# Test authentication
python -c "from auth import auth; print('✓ Auth module loaded')"

# Test validators
python -c "from utils import validators; print('✓ Validators loaded')"
```

## 🤝 Contributing

Contributions are welcome! The modular structure makes it easy to contribute:

### Development Setup
1. Fork or clone the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes in the appropriate module
4. Test your changes thoroughly
5. Commit with clear messages
6. Submit a pull request

### Adding New Features

**New database operations?**
- Add functions to `database/models.py`

**New authentication feature?**
- Add to `auth/auth.py`

**New UI component?**
- Create in appropriate file in `ui/`

**New validation rules?**
- Add to `utils/validators.py`

## 📚 Further Improvements

Future enhancements could include:
- Advanced user management and roles
- Inventory analytics and reporting
- Multi-user collaboration features
- Backup and restore functionality
- Logging and audit trails
- ✅ **Unit tests for each module** (COMPLETED)
- REST API endpoints
- Configuration file support
- Data export/import functionality
- Barcode scanning integration
- Multi-location inventory tracking

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support & Documentation

- See `REFACTORING_SUMMARY.md` for detailed information about the modular architecture
- Check `tests/README.md` for comprehensive testing documentation
- Review individual module docstrings for function-level documentation
- Check `config.py` for all available configuration options

---

**Built with ❤️ using Python, SQLite, and Tkinter**

**Current Structure:** Modular Architecture (v2.0 Refactored)  
**Last Updated:** February 2026  
**Test Coverage:** 17 comprehensive test cases ✅
