# Inventory Management System

A comprehensive supermarket inventory management system built with Python and SQLite, featuring both console and graphical user interfaces.

## 🚀 Features

### Core Functionality
- **Inventory Management**: Add, view, update, and delete inventory items
- **Category Management**: Organize products into categories with descriptions
- **Supplier Management**: Track supplier information and contact details
- **Transaction Tracking**: Log stock movements (IN/OUT) with dates and notes
- **Search & Filter**: Find items quickly by name or category
- **Data Persistence**: SQLite database for reliable data storage

### User Interfaces
- **Console Interface**: Traditional command-line interface (`main.py`)
- **Graphical Interface**: Modern GUI with tabbed layout (`gui.py`)
- **Dual Access**: Both interfaces share the same database

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

### Option 1: Graphical User Interface (Recommended)
```bash
python gui.py
```

### Option 2: Console Interface
```bash
python main.py
```

The first run will automatically create the SQLite database (`inventory.db`) and all necessary tables.

## 📊 Database Schema

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

### Main Interface
- **Tabbed Layout**: Organized sections for different management areas
- **Status Bar**: Real-time feedback for operations
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

## 💻 Console Interface

The console interface provides the same functionality through a menu-driven system:

```
Supermarket Inventory Management System
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

16. Exit
```

## 🔧 Technical Details

### Architecture
- **Backend**: Python with SQLite3
- **Frontend**: tkinter for GUI
- **Database**: SQLite (`inventory.db`)
- **Design Pattern**: Modular functions with clear separation of concerns

### Key Files
- `main.py` - Core business logic and console interface
- `gui.py` - Graphical user interface
- `inventory.db` - SQLite database (created automatically)

### Error Handling
- Input validation for all forms
- SQL injection protection with parameterized queries
- Graceful error handling for database operations
- User-friendly error messages

## 📝 Usage Examples

### Adding an Item (GUI)
1. Open the GUI: `python gui.py`
2. Navigate to the Inventory tab
3. Fill in the form fields (name, category, quantity, price)
4. Click "Add Item"

### Adding a Transaction (Console)
1. Run: `python main.py`
2. Select option 13 (Add Transaction)
3. Enter item ID, transaction type (IN/OUT), quantity, and date
4. Add optional notes

### Searching Items (GUI)
1. In the Inventory tab, use the search box
2. Type item name or category
3. Click "Search" to filter results

## 🔄 Data Synchronization

Both interfaces share the same database, allowing:
- Seamless switching between GUI and console
- Real-time data updates across interfaces
- Consistent data integrity

## 🐛 Troubleshooting

### Common Issues

**GUI won't open:**
- Ensure tkinter is installed: `pip install tk`
- Check Python version compatibility

**Database errors:**
- Ensure write permissions in the project directory
- Check if `inventory.db` is not locked by another process

**Import errors:**
- Verify all files are in the same directory
- Check Python path settings

### Getting Help

1. Check the error messages carefully
2. Ensure all requirements are met
3. Verify file permissions and directory structure

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check existing issues for solutions
- Review the documentation carefully

---

**Built with ❤️ using Python and SQLite**
