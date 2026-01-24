# Supermarket Inventory Management System with SQLite Integration
import sqlite3
import hashlib
from datetime import datetime



DB_NAME = 'inventory.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_categories_table():
    """Create a categories table to manage product categories"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_suppliers_table():
    """Create a suppliers table to track supplier information"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_transactions_table():
    """Create a transactions table to log inventory movements"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            transaction_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (item_id) REFERENCES inventory (id)
        )
    ''')
    conn.commit()
    conn.close()

def create_users_table():
    """Create a users table for authentication"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_value):
    """Verify a password against its hash"""
    return hash_password(password) == hash_value

def create_user(username, password, email=None, role='user'):
    """Create a new user"""
    conn = sqlite3.connect(DB_NAME)
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
    """Authenticate a user"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and verify_password(password, user[2]):
        return {'id': user[0], 'username': user[1], 'role': user[3]}
    return None

def get_all_users():
    """Get all users (for admin purposes)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, username, email, role, created_at FROM users')
    users = c.fetchall()
    conn.close()
    return users

def add_item(name, category, quantity, price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO inventory (name, category, quantity, price) VALUES (?, ?, ?, ?)',
              (name, category, quantity, price))
    conn.commit()
    conn.close()

def view_items():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()
    conn.close()
    return items

def update_item(item_id, name=None, category=None, quantity=None, price=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    fields = []
    values = []
    if name is not None:
        fields.append('name = ?')
        values.append(name)
    if category is not None:
        fields.append('category = ?')
        values.append(category)
    if quantity is not None:
        fields.append('quantity = ?')
        values.append(quantity)
    if price is not None:
        fields.append('price = ?')
        values.append(price)
    
    if not fields:
        conn.close()
        return
        
    values.append(item_id)
    sql = f'UPDATE inventory SET {", ".join(fields)} WHERE id = ?'
    c.execute(sql, values)
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Category Management Functions
def add_category(name, description=None):
    """Add a new category"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()

def view_categories():
    """View all categories"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM categories')
    categories = c.fetchall()
    conn.close()
    return categories

def update_category(category_id, name=None, description=None):
    """Update a category"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    fields = []
    values = []
    if name is not None:
        fields.append('name = ?')
        values.append(name)
    if description is not None:
        fields.append('description = ?')
        values.append(description)
    
    if not fields:
        conn.close()
        return
        
    values.append(category_id)
    sql = f'UPDATE categories SET {", ".join(fields)} WHERE id = ?'
    c.execute(sql, values)
    conn.commit()
    conn.close()

def delete_category(category_id):
    """Delete a category"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()

# Supplier Management Functions
def add_supplier(name, contact_person=None, phone=None, email=None, address=None):
    """Add a new supplier"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO suppliers (name, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?)',
              (name, contact_person, phone, email, address))
    conn.commit()
    conn.close()

def view_suppliers():
    """View all suppliers"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM suppliers')
    suppliers = c.fetchall()
    conn.close()
    return suppliers

def update_supplier(supplier_id, name=None, contact_person=None, phone=None, email=None, address=None):
    """Update a supplier"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    fields = []
    values = []
    if name is not None:
        fields.append('name = ?')
        values.append(name)
    if contact_person is not None:
        fields.append('contact_person = ?')
        values.append(contact_person)
    if phone is not None:
        fields.append('phone = ?')
        values.append(phone)
    if email is not None:
        fields.append('email = ?')
        values.append(email)
    if address is not None:
        fields.append('address = ?')
        values.append(address)
    
    if not fields:
        conn.close()
        return
        
    values.append(supplier_id)
    sql = f'UPDATE suppliers SET {", ".join(fields)} WHERE id = ?'
    c.execute(sql, values)
    conn.commit()
    conn.close()

def delete_supplier(supplier_id):
    """Delete a supplier"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM suppliers WHERE id = ?', (supplier_id,))
    conn.commit()
    conn.close()

# Transaction Management Functions
def add_transaction(item_id, transaction_type, quantity, date, notes=None):
    """Add a new transaction"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO transactions (item_id, transaction_type, quantity, date, notes) VALUES (?, ?, ?, ?, ?)',
              (item_id, transaction_type, quantity, date, notes))
    conn.commit()
    conn.close()

def view_transactions():
    """View all transactions"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT t.*, i.name as item_name 
        FROM transactions t 
        LEFT JOIN inventory i ON t.item_id = i.id 
        ORDER BY t.date DESC
    ''')
    transactions = c.fetchall()
    conn.close()
    return transactions

def view_transactions_by_item(item_id):
    """View transactions for a specific item"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT t.*, i.name as item_name 
        FROM transactions t 
        LEFT JOIN inventory i ON t.item_id = i.id 
        WHERE t.item_id = ?
        ORDER BY t.date DESC
    ''', (item_id,))
    transactions = c.fetchall()
    conn.close()
    return transactions

def login():
    """Handle user login - IDE Friendly Version"""
    print("\n=== LOGIN ===")
    print("Note: Password will be visible (IDE terminal mode), since the getpass module was not working :(")
    username = input("Username: ")
    password = input("Password: ")  # Regular input for IDE compatibility
    
    user = authenticate_user(username, password)
    if user:
        print(f"Welcome, {user['username']}!")
        return user
    else:
        print("Invalid username or password!")
        return None

def setup_first_time():
    """Setup first-time admin user - IDE Friendly Version"""
    print("\n=== FIRST TIME SETUP ===")
    print("Creating default admin user...")
    print("Note: Password will be visible (IDE terminal mode)")
    
    while True:
        username = input("Enter admin username: ").strip()
        if username:
            break
        print("Username cannot be empty!")
    
    while True:
        password = input("Enter admin password: ")  # Regular input for IDE compatibility
        if len(password) >= 4:
            break
        print("Password must be at least 4 characters!")
    
    email = input("Enter admin email (optional): ").strip() or None
    
    if create_user(username, password, email, 'admin'):
        print(f"Admin user '{username}' created successfully!")
        return True
    else:
        print("Failed to create admin user!")
        return False

def main():
    init_db()
    create_categories_table()
    create_suppliers_table()
    create_transactions_table()
    create_users_table()
    
    # Check if any users exist
    users = get_all_users()
    if not users:
        print("No users found. Setting up first admin user.")
        if not setup_first_time():
            return
    
    # Login
    current_user = None
    while not current_user:
        current_user = login()
    
    # Main menu
    while True:
        print(f"\nMetlab Supermarket Inventory Management System")
        print(f"Logged in as: {current_user['username']} ({current_user['role']})")
        print("=== INVENTORY MANAGEMENT ===")
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Delete Item")
        print("\n=== CATEGORY MANAGEMENT ===")
        print("5. Add Category")
        print("6. View Categories")
        print("7. Update Category")
        print("8. Delete Category")
        print("\n=== SUPPLIER MANAGEMENT ===")
        print("9. Add Supplier")
        print("10. View Suppliers")
        print("11. Update Supplier")
        print("12. Delete Supplier")
        print("\n=== TRANSACTION MANAGEMENT ===")
        print("13. Add Transaction")
        print("14. View All Transactions")
        print("15. View Item Transactions")
        
        if current_user['role'] == 'admin':
            print("\n=== USER MANAGEMENT ===")
            print("16. Add User")
            print("17. View Users")
            print("18. Logout")
            print("19. Exit")
        else:
            print("\n16. Logout")
            print("17. Exit")
            
        choice = input("Select an option: ")
        
        if choice == '1':
            name = input("Item name: ")
            category = input("Category: ")
            quantity = int(input("Quantity: "))
            price = float(input("Price: "))
            add_item(name, category, quantity, price)
            print("Item added.")
            
        elif choice == '2':
            items = view_items()
            print("\nID | Name | Category | Quantity | Price")
            for item in items:
                print(f"{item[0]} | {item[1]} | {item[2]} | {item[3]} | ${item[4]:.2f}")
               
        elif choice == '3':
            item_id = int(input("Enter item ID to update: "))
            print("Leave field blank to keep current value.")
            name = input("New name: ") or None
            category = input("New category: ") or None
            quantity = input("New quantity: ")
            quantity = int(quantity) if quantity else None
            price = input("New price: ")
            price = float(price) if price else None
            update_item(item_id, name, category, quantity, price)
            print("Item updated.")
            
        elif choice == '4':
            item_id = int(input("Enter item ID to delete: "))
            delete_item(item_id)
            print("Item deleted.")
            
        elif choice == '5':
            name = input("Category name: ")
            description = input("Description (optional): ") or None
            add_category(name, description)
            print("Category added.")
            
        elif choice == '6':
            categories = view_categories()
            print("\nID | Name | Description")
            for cat in categories:
                print(f"{cat[0]} | {cat[1]} | {cat[2] or 'N/A'}")
                
        elif choice == '7':
            cat_id = int(input("Enter category ID to update: "))
            print("Leave field blank to keep current value.")
            name = input("New name: ") or None
            description = input("New description: ") or None
            update_category(cat_id, name, description)
            print("Category updated.")
            
        elif choice == '8':
            cat_id = int(input("Enter category ID to delete: "))
            delete_category(cat_id)
            print("Category deleted.")
            
        elif choice == '9':
            name = input("Supplier name: ")
            contact = input("Contact person (optional): ") or None
            phone = input("Phone (optional): ") or None
            email = input("Email (optional): ") or None
            address = input("Address (optional): ") or None
            add_supplier(name, contact, phone, email, address)
            print("Supplier added.")
            
        elif choice == '10':
            suppliers = view_suppliers()
            print("\nID | Name | Contact | Phone | Email | Address")
            for sup in suppliers:
                print(f"{sup[0]} | {sup[1]} | {sup[2] or 'N/A'} | {sup[3] or 'N/A'} | {sup[4] or 'N/A'} | {sup[5] or 'N/A'}")
               
        elif choice == '11':
            sup_id = int(input("Enter supplier ID to update: "))
            print("Leave field blank to keep current value.")
            name = input("New name: ") or None
            contact = input("New contact person: ") or None
            phone = input("New phone: ") or None
            email = input("New email: ") or None
            address = input("New address: ") or None
            update_supplier(sup_id, name, contact, phone, email, address)
            print("Supplier updated.")
            
        elif choice == '12':
            sup_id = int(input("Enter supplier ID to delete: "))
            delete_supplier(sup_id)
            print("Supplier deleted.")
            
        elif choice == '13':
            item_id = int(input("Item ID: "))
            trans_type = input("Transaction type (IN/OUT): ").upper()
            quantity = int(input("Quantity: "))
            date = input("Date (YYYY-MM-DD): ")
            notes = input("Notes (optional): ") or None
            add_transaction(item_id, trans_type, quantity, date, notes)
            print("Transaction added.")
            
        elif choice == '14':
            transactions = view_transactions()
            print("\nID | Item | Type | Quantity | Date | Notes")
            for trans in transactions:
                print(f"{trans[0]} | {trans[6]} | {trans[2]} | {trans[3]} | {trans[4]} | {trans[5] or 'N/A'}")
            
        elif choice == '15':
            item_id = int(input("Enter item ID to view transactions: "))
            transactions = view_transactions_by_item(item_id)
            print(f"\nTransactions for Item ID {item_id}:")
            print("ID | Type | Quantity | Date | Notes")
            for trans in transactions:
                print(f"{trans[0]} | {trans[2]} | {trans[3]} | {trans[4]} | {trans[5] or 'N/A'}")
        
        # Admin-only options
        elif current_user['role'] == 'admin':
            if choice == '16':
                username = input("New username: ")
                password = input("New password: ")  # Regular input for IDE compatibility
                email = input("Email (optional): ") or None
                role = input("Role (user/admin): ").lower() or 'user'
                
                if role not in ['user', 'admin']:
                    role = 'user'
                
                if create_user(username, password, email, role):
                    print(f"User '{username}' created successfully!")
                else:
                    print("Failed to create user (username may already exist)!")
                    
            elif choice == '17':
                users = get_all_users()
                print("\nID | Username | Email | Role | Created At")
                for user in users:
                    print(f"{user[0]} | {user[1]} | {user[2] or 'N/A'} | {user[3]} | {user[4]}")
                    
            elif choice == '18':
                print("Logging out...")
                current_user = None
                while not current_user:
                    current_user = login()
                    
            elif choice == '19':
                print("Goodbye!")
                break
        
        # Regular user options
        else:
            if choice == '16':
                print("Logging out...")
                current_user = None
                while not current_user:
                    current_user = login()
                    
            elif choice == '17':
                print("Goodbye!")
                break
                
            else:
                print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
