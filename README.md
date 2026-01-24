# Metlab Supermarket Inventory Management System

A comprehensive supermarket inventory management system built with Python and SQLite, featuring both console and graphical user interfaces with secure user authentication. Designed for Metlab Supermarket operations.

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

### User Interfaces
- **Console Interface**: Traditional command-line interface (`main.py`) - IDE-friendly version
- **Graphical Interface**: Modern GUI with tabbed layout (`gui.py`) with full authentication
- **Dual Access**: Both interfaces share the same database and authentication
- **Cross-Platform Compatibility**: Works in IDE terminals and system terminals

## 📋 System Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- SQLite3 (included with Python)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "INVENTORY MANAGEMENT SYSTEM 2"
   ```

2. **Verify Python installation**
   ```bash
   python --version
   ```

3. **Install dependencies** (if needed)
   ```bash
   pip install tk
   ```

## 🎯 Quick Start

### First Time Setup
The first time you run either interface, you'll be prompted to create an admin account:

**GUI Setup (Recommended):**
```bash
python gui.py
```
- Follow the prompts to create the first admin user
- Use the modern login window to access the system
- Full graphical interface with user management

**Console Setup:**
```bash
python main.py
```
- Follow the console prompts to create the first admin user
- Login with your credentials
- IDE-friendly version (passwords visible in development)

### Development vs Production

#### Development (IDE Terminals)
```bash
python main.py
```
- ✅ Works in any IDE terminal (VS Code, PyCharm, etc.)
- ⚠️ Passwords visible during input
- ✅ Full functionality maintained

#### Production (System Terminals)
```bash
# Use Command Prompt or PowerShell for secure password input
python main_backup_secure.py
```
- ✅ Passwords hidden during input
- ✅ Production-ready security
- ✅ Same functionality

### User Roles

#### Admin Users
- Full access to all inventory features
- **User Management**: Create, view, and manage user accounts
- **System Administration**: Complete control over the system
- **GUI Access**: Additional "Users" tab and menu options

#### Regular Users
- Standard inventory management features
- Can add, update, and view inventory items
- Can manage categories, suppliers, and transactions
- **Limited Access**: Cannot manage user accounts

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

## 💻 Console Interface

The console interface provides the same functionality through a menu-driven system with authentication:

```
=== LOGIN ===
Note: Password will be visible (IDE terminal mode)
Username: [your_username]
Password: [your_password]

Metlab Supermarket Inventory Management System
Logged in as: [username] ([role])
=== INVENTORY MANAGEMENT ===
1. Add Item
2. View Items
3. Update Item
4. Delete Item

=== CATEGORY MANAGEMENT ===
5. Add Category
6. View Categories
7. Update Category
8. Delete Category

=== SUPPLIER MANAGEMENT ===
9. Add Supplier
10. View Suppliers
11. Update Supplier
12. Delete Supplier

=== TRANSACTION MANAGEMENT ===
13. Add Transaction
14. View All Transactions
15. View Item Transactions

=== USER MANAGEMENT === (Admin only)
16. Add User
17. View Users
18. Logout
19. Exit
```

### Console Features
- **IDE-Friendly**: Works in VS Code, PyCharm, and other IDE terminals
- **Visible Passwords**: Development-friendly (passwords shown during input)
- **Full Functionality**: All inventory management features available
- **User Management**: Admin can create and manage users
- **Role-Based Access**: Different menus for admin vs regular users

## 🔧 Technical Details

### Authentication Security
- **Password Hashing**: SHA-256 algorithm for secure password storage
- **Input Validation**: Proper validation for usernames and passwords
- **Session Management**: Secure login/logout functionality
- **Role-Based Access**: Different permissions for admin and regular users

### Architecture
- **Backend**: Python with SQLite3
- **Frontend**: tkinter for GUI
- **Database**: SQLite (`inventory.db`)
- **Design Pattern**: Modular functions with clear separation of concerns

### Key Files
- `main.py` - Core business logic, authentication, and IDE-friendly console interface
- `main_backup_secure.py` - Original secure version with hidden passwords (for production)
- `gui.py` - Graphical user interface with full authentication
- `inventory.db` - SQLite database (created automatically)

### Error Handling
- Input validation for all forms
- SQL injection protection with parameterized queries
- Graceful error handling for database operations
- User-friendly error messages
- Authentication failure handling

## 📝 Usage Examples

**First-Time Admin Setup**
1. Run `python gui.py` or `python main.py`
2. Follow the prompts to create an admin account
3. Login with your new admin credentials

### Adding a User (Admin Only)
**GUI:**
1. Login as admin
2. Go to Users tab or menu → Add User
3. Fill in username, password, email, and role
4. Click "Create User"

**Console:**
1. Login as admin
2. Select option 16 (Add User)
3. Enter user details when prompted
4. Note: Password will be visible in IDE terminal mode

### Adding an Item (GUI)
1. Navigate to the Inventory tab
2. Fill in the form fields (name, category, quantity, price)
3. Click "Add Item"

### Adding a Transaction (Console)
1. Login to the system
2. Select option 13 (Add Transaction)
3. Enter item ID, transaction type (IN/OUT), quantity, and date
4. Add optional notes

### Searching Items (GUI)
1. In the Inventory tab, use the search box
2. Type item name or category
3. Click "Search" to filter results

### Development Workflow
**For development in IDE terminals:**
```bash
python main.py  # IDE-friendly version
```

**For production deployment:**
```bash
python main_backup_secure.py  # Secure version with hidden passwords
```

## 🔄 Data Synchronization

Both interfaces share the same database and authentication system:
- Seamless switching between GUI and console
- Real-time data updates across interfaces
- Consistent user authentication across both interfaces
- Shared user accounts and roles

## 🐛 Troubleshooting

### Common Issues

**Login Issues:**
- Ensure correct username and password
- Check if user account exists (admin can view users)
- Passwords are case-sensitive
- For IDE terminals: Passwords will be visible during input

**GUI won't open:**
- Ensure tkinter is installed: `pip install tk`
- Check Python version compatibility (3.7+ required)

**Console Input Issues:**
- **IDE Terminals**: Use `python main.py` (passwords visible)
- **System Terminals**: Use `python main_backup_secure.py` (passwords hidden)
- **VS Code/PyCharm**: Console version works with visible passwords

**Database errors:**
- Ensure write permissions in the project directory
- Check if `inventory.db` is not locked by another process

**First-time setup issues:**
- Ensure admin username is at least 1 character
- Password must be at least 4 characters
- Check database write permissions
- Try running in system terminal if IDE setup fails

### Getting Help

1. Check the error messages carefully
2. Ensure all requirements are met
3. Verify file permissions and directory structure
4. Check if users table exists in database

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (both GUI and console interfaces)
5. Test in both IDE terminals and system terminals
6. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check existing issues for solutions
- Review the documentation carefully

---

**Built with ❤️ for Metlab Supermarket using Python, SQLite, and Tkinter**
