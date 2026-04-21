import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import os
import config
from database import models
from auth import auth
from ui.login import LoginWindow
from ui.windows import InventoryManagementGUI

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def init_database():
    """Initialize all database tables"""
    models.init_db()
    models.create_categories_table()
    models.create_suppliers_table()
    models.create_transactions_table()
    models.create_users_table()
    models.create_measurement_units_table()
    models.init_default_measurement_units()
    models.update_database_schema()  # Update existing database


def create_first_admin():
    """Create first admin user if no users exist. Returns True if first admin was created."""
    users = auth.get_all_users()
    if users:
        return False  # Users already exist
    
    # Create first admin user
    setup_root = tk.Tk()
    setup_root.iconbitmap("ui/images/favicon.ico")
    setup_root.geometry(config.SETUP_WINDOW_GEOMETRY)
    setup_root.withdraw()  # Hide main window

    username = simpledialog.askstring("First Time Setup", "Enter admin username:")
    if not username:
        setup_root.destroy()
        return False
    
    password = simpledialog.askstring("First Time Setup", "Enter admin password:", show='*')
    if not password or len(password) < config.MIN_PASSWORD_LENGTH:
        messagebox.showerror("Error", f"Password must be at least {config.MIN_PASSWORD_LENGTH} characters!")
        setup_root.destroy()
        return False
    
    email = simpledialog.askstring("First Time Setup", "Enter admin email (optional):")
    
    if auth.create_user(username, password, email or None, config.ROLE_ADMIN):
        messagebox.showinfo("Success", f"Admin user '{username}' created successfully!")
    else:
        messagebox.showerror("Error", "Failed to create admin user!")
    
    setup_root.destroy()
    return True  # First admin was created


def main():
    """Main application entry point"""
    # Initialize database
    init_database()
    
    # Create first admin user if needed
    first_admin_created = create_first_admin()
    
    # Show login window (either immediately or after admin creation)
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
    
    # If login successful, show main application
    if login_window.authenticated_user:
        main_root = tk.Tk()
        app = InventoryManagementGUI(main_root, login_window.authenticated_user)
        main_root.mainloop()


if __name__ == "__main__":
    main()
