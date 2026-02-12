import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import config
from database import models
from auth import auth
from ui.dialogs import AddUserDialog


class InventoryManagementGUI:
    """Main application window class"""
    
    def __init__(self, root, user):
        self.root = root
        self.current_user = user
        self.root.title(f"{config.MAIN_WINDOW_TITLE} - {user['username']} ({user['role']})")
        self.root.geometry(config.MAIN_WINDOW_GEOMETRY)
        
        # Initialize database
        self.init_database()
        
        # Create menu bar
        self.create_menu()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_inventory_tab()
        self.create_categories_tab()
        self.create_suppliers_tab()
        self.create_transactions_tab()
        
        # Admin-only user management tab
        if user['role'] == config.ROLE_ADMIN:
            self.create_users_tab()
        
        # Status bar
        self.status_bar = tk.Label(root, text=f"Logged in as: {user['username']} ({user['role']})", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def init_database(self):
        """Initialize all database tables"""
        models.init_db()
        models.create_categories_table()
        models.create_suppliers_table()
        models.create_transactions_table()
        models.create_users_table()
        
    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # User menu (admin only)
        if self.current_user['role'] == config.ROLE_ADMIN:
            user_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Users", menu=user_menu)
            user_menu.add_command(label="Add User", command=self.show_add_user_dialog)
            user_menu.add_command(label="View Users", command=self.view_users_dialog)
            
            # Database menu (admin only)
            db_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Database", menu=db_menu)
            db_menu.add_command(label="Clear All Data", command=self.clear_all_data)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            
    def show_about(self):
        """Show about dialog"""
        about_text = """Inventory Management System v2.0
        
Features:
• Inventory Management
• Category Management  
• Supplier Management
• Transaction Tracking
• User Authentication
• Role-based Access Control

Developed with Python and Tkinter"""
        messagebox.showinfo("About", about_text)
        
    def show_add_user_dialog(self):
        """Show add user dialog"""
        try:
            AddUserDialog(self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open add user dialog: {e}")
            
    def view_users_dialog(self):
        """Show view users dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Users")
        dialog.geometry("600x400")
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Users", font=config.DEFAULT_FONT_LABEL).pack(pady=5)
        
        # Treeview for users
        columns = ('ID', 'Username', 'Email', 'Role', 'Created At')
        self.users_tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Button frame
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add User", command=self.show_add_user_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_users).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.refresh_users()
        
    def delete_user(self):
        """Delete selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user to delete!")
            return
            
        user_data = self.users_tree.item(selected[0])['values']
        user_id = user_data[0]
        username = user_data[1]
        role = user_data[3]
        
        # Prevent self-deletion
        if user_id == self.current_user['id']:
            messagebox.showerror("Error", "You cannot delete your own account!")
            return
            
        # Confirm deletion
        confirm_message = f"Are you sure you want to delete user '{username}'?\n\n"
        confirm_message += f"Username: {username}\n"
        confirm_message += f"Role: {role}\n\n"
        confirm_message += "This action cannot be undone!"
        
        if not messagebox.askyesno("Confirm Delete User", confirm_message):
            return
            
        # Delete user
        success, message = auth.delete_user(user_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_users()
        else:
            messagebox.showerror("Error", message)
                
    def refresh_users(self):
        """Refresh the users tree view"""
        if hasattr(self, 'users_tree'):
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
                
            users = auth.get_all_users()
            for user in users:
                self.users_tree.insert('', 'end', values=user)
                
    def create_users_tab(self):
        """Create the users management tab (admin only)"""
        self.users_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.users_frame, text="Users")
        
        # Button frame
        button_frame = ttk.Frame(self.users_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add User", command=self.show_add_user_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete User", command=self.delete_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_users).pack(side=tk.LEFT, padx=5)
        
        # Treeview for users
        columns = ('ID', 'Username', 'Email', 'Role', 'Created At')
        self.users_tree = ttk.Treeview(self.users_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(self.users_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        self.refresh_users()
        
    def create_inventory_tab(self):
        """Create the inventory management tab"""
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="Inventory")
        
        # Left panel for form
        left_frame = ttk.Frame(self.inventory_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Form fields
        ttk.Label(left_frame, text="Inventory Management", font=config.DEFAULT_FONT_LABEL).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(left_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.item_name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.item_name_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(left_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.item_category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(left_frame, textvariable=self.item_category_var, width=28)
        self.category_combo.grid(row=2, column=1, pady=5)
        
        ttk.Label(left_frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.item_quantity_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.item_quantity_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Label(left_frame, text="Price:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.item_price_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.item_price_var, width=30).grid(row=4, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Item", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Item", command=self.update_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Item", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_inventory_form).pack(side=tk.LEFT, padx=5)
        
        # Right panel for list
        right_frame = ttk.Frame(self.inventory_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Inventory Items", font=config.DEFAULT_FONT_LABEL).pack(pady=5)
        
        # Treeview for inventory
        columns = ('ID', 'Name', 'Category', 'Quantity', 'Price')
        self.inventory_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        self.inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click for editing
        self.inventory_tree.bind('<Double-1>', self.on_inventory_double_click)
        
        # Search frame
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="Search", command=self.search_inventory).pack(side=tk.LEFT)
        
        # Load initial data
        self.refresh_inventory()
        self.update_categories_combo()
        
    def create_categories_tab(self):
        """Create the categories management tab"""
        self.categories_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.categories_frame, text="Categories")
        
        # Left panel for form
        left_frame = ttk.Frame(self.categories_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Category Management", font=config.DEFAULT_FONT_LABEL).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(left_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.category_name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.category_name_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(left_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_desc_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.category_desc_var, width=30).grid(row=2, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Category", command=self.add_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Category", command=self.update_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Category", command=self.delete_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_category_form).pack(side=tk.LEFT, padx=5)
        
        # Right panel for list
        right_frame = ttk.Frame(self.categories_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Categories", font=config.DEFAULT_FONT_LABEL).pack(pady=5)
        
        # Treeview for categories
        columns = ('ID', 'Name', 'Description')
        self.categories_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.categories_tree.heading(col, text=col)
            self.categories_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.categories_tree.yview)
        self.categories_tree.configure(yscrollcommand=scrollbar.set)
        
        self.categories_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.categories_tree.bind('<Double-1>', self.on_category_double_click)
        
        ttk.Button(right_frame, text="Refresh", command=self.refresh_categories).pack(pady=5)
        
        # Load initial data
        self.refresh_categories()
        
    def create_suppliers_tab(self):
        """Create the suppliers management tab"""
        self.suppliers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.suppliers_frame, text="Suppliers")
        
        # Left panel for form
        left_frame = ttk.Frame(self.suppliers_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Supplier Management", font=config.DEFAULT_FONT_LABEL).grid(row=0, column=0, columnspan=2, pady=10)
        
        fields = [
            ("Name:", "supplier_name_var"),
            ("Contact Person:", "supplier_contact_var"),
            ("Phone:", "supplier_phone_var"),
            ("Email:", "supplier_email_var"),
            ("Address:", "supplier_address_var")
        ]
        
        for i, (label, var_name) in enumerate(fields, 1):
            ttk.Label(left_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            var = tk.StringVar()
            setattr(self, var_name, var)
            ttk.Entry(left_frame, textvariable=var, width=30).grid(row=i, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Supplier", command=self.add_supplier).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Supplier", command=self.update_supplier).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Supplier", command=self.delete_supplier).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_supplier_form).pack(side=tk.LEFT, padx=5)
        
        # Right panel for list
        right_frame = ttk.Frame(self.suppliers_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Suppliers", font=config.DEFAULT_FONT_LABEL).pack(pady=5)
        
        # Treeview for suppliers
        columns = ('ID', 'Name', 'Contact', 'Phone', 'Email', 'Address')
        self.suppliers_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.suppliers_tree.heading(col, text=col)
            self.suppliers_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.suppliers_tree.yview)
        self.suppliers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.suppliers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.suppliers_tree.bind('<Double-1>', self.on_supplier_double_click)
        
        ttk.Button(right_frame, text="Refresh", command=self.refresh_suppliers).pack(pady=5)
        
        # Load initial data
        self.refresh_suppliers()
        
    def create_transactions_tab(self):
        """Create the transactions management tab"""
        self.transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.transactions_frame, text="Transactions")
        
        # Left panel for form
        left_frame = ttk.Frame(self.transactions_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Transaction Management", font=config.DEFAULT_FONT_LABEL).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(left_frame, text="Item:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.transaction_item_var = tk.StringVar()
        self.transaction_item_combo = ttk.Combobox(left_frame, textvariable=self.transaction_item_var, width=28)
        self.transaction_item_combo.grid(row=1, column=1, pady=5)
        
        ttk.Label(left_frame, text="Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.transaction_type_var = tk.StringVar()
        type_combo = ttk.Combobox(left_frame, textvariable=self.transaction_type_var, width=28, 
                                 values=[config.TRANSACTION_TYPE_IN, config.TRANSACTION_TYPE_OUT])
        type_combo.grid(row=2, column=1, pady=5)
        
        ttk.Label(left_frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.transaction_quantity_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.transaction_quantity_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Label(left_frame, text="Date:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.transaction_date_var = tk.StringVar()
        self.transaction_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(left_frame, textvariable=self.transaction_date_var, width=30).grid(row=4, column=1, pady=5)
        
        ttk.Label(left_frame, text="Notes:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.transaction_notes_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.transaction_notes_var, width=30).grid(row=5, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Transaction", command=self.add_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_transaction_form).pack(side=tk.LEFT, padx=5)
        
        # Right panel for list
        right_frame = ttk.Frame(self.transactions_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Transactions", font=config.DEFAULT_FONT_LABEL).pack(pady=5)
        
        # Treeview for transactions
        columns = ('ID', 'Item', 'Type', 'Quantity', 'Date', 'Notes')
        self.transactions_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(right_frame, text="Refresh", command=self.refresh_transactions).pack(pady=5)
        
        # Load initial data
        self.refresh_transactions()
        self.update_items_combo()
        
    # ============ Inventory Methods ============
    def add_item(self):
        """Add a new inventory item"""
        try:
            name = self.item_name_var.get()
            category = self.item_category_var.get()
            quantity = int(self.item_quantity_var.get())
            price = float(self.item_price_var.get())
            
            if not name or not category:
                messagebox.showerror("Error", "Name and Category are required!")
                return
            
            models.add_item(name, category, quantity, price)
            self.clear_inventory_form()
            self.refresh_inventory()
            self.status_bar.config(text=f"Item '{name}' added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price!")
            
    def update_item(self):
        """Update selected inventory item"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to update!")
            return
            
        try:
            item_id = self.inventory_tree.item(selected[0])['values'][0]
            name = self.item_name_var.get()
            category = self.item_category_var.get()
            quantity = self.item_quantity_var.get()
            price = self.item_price_var.get()
            
            # Handle empty strings vs None values
            name = name if name.strip() else None
            category = category if category.strip() else None
            quantity = int(quantity) if quantity else None
            price = float(price) if price else None
            
            models.update_item(item_id, name, category, quantity, price)
            self.clear_inventory_form()
            self.refresh_inventory()
            self.status_bar.config(text=f"Item ID {item_id} updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price!")
            
    def delete_item(self):
        """Delete selected inventory item"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            item_id = self.inventory_tree.item(selected[0])['values'][0]
            models.delete_item(item_id)
            self.clear_inventory_form()
            self.refresh_inventory()
            self.status_bar.config(text=f"Item ID {item_id} deleted successfully!")
            
    def clear_inventory_form(self):
        """Clear inventory form fields"""
        self.item_name_var.set("")
        self.item_category_var.set("")
        self.item_quantity_var.set("")
        self.item_price_var.set("")
        
    def refresh_inventory(self):
        """Refresh inventory tree view"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        items = models.view_items()
        for item in items:
            self.inventory_tree.insert('', 'end', values=item)
            
    def search_inventory(self):
        """Search inventory items"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self.refresh_inventory()
            return
            
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        items = models.view_items()
        for item in items:
            if (search_term in str(item[1]).lower() or 
                search_term in str(item[2]).lower()):
                self.inventory_tree.insert('', 'end', values=item)
                
    def on_inventory_double_click(self, event):
        """Handle double click on inventory item"""
        selected = self.inventory_tree.selection()
        if selected:
            item = self.inventory_tree.item(selected[0])['values']
            self.item_name_var.set(item[1])
            self.item_category_var.set(item[2])
            self.item_quantity_var.set(item[3])
            self.item_price_var.set(item[4])
            
    # ============ Category Methods ============
    def add_category(self):
        """Add a new category"""
        name = self.category_name_var.get()
        description = self.category_desc_var.get()
        
        if not name:
            messagebox.showerror("Error", "Category name is required!")
            return
            
        models.add_category(name, description)
        self.clear_category_form()
        self.refresh_categories()
        self.update_categories_combo()
        self.status_bar.config(text=f"Category '{name}' added successfully!")
        
    def update_category(self):
        """Update selected category"""
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to update!")
            return
            
        category_id = self.categories_tree.item(selected[0])['values'][0]
        name = self.category_name_var.get()
        description = self.category_desc_var.get()
        
        name = name if name else None
        description = description if description else None
        
        models.update_category(category_id, name, description)
        self.clear_category_form()
        self.refresh_categories()
        self.update_categories_combo()
        self.status_bar.config(text=f"Category ID {category_id} updated successfully!")
        
    def delete_category(self):
        """Delete selected category"""
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?"):
            category_id = self.categories_tree.item(selected[0])['values'][0]
            models.delete_category(category_id)
            self.clear_category_form()
            self.refresh_categories()
            self.update_categories_combo()
            self.status_bar.config(text=f"Category ID {category_id} deleted successfully!")
            
    def clear_category_form(self):
        """Clear category form fields"""
        self.category_name_var.set("")
        self.category_desc_var.set("")
        
    def refresh_categories(self):
        """Refresh categories tree view"""
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
            
        categories = models.view_categories()
        for category in categories:
            self.categories_tree.insert('', 'end', values=category)
            
    def on_category_double_click(self, event):
        """Handle double click on category"""
        selected = self.categories_tree.selection()
        if selected:
            category = self.categories_tree.item(selected[0])['values']
            self.category_name_var.set(category[1])
            self.category_desc_var.set(category[2] if category[2] else "")
            
    # ============ Supplier Methods ============
    def add_supplier(self):
        """Add a new supplier"""
        name = self.supplier_name_var.get()
        contact = self.supplier_contact_var.get()
        phone = self.supplier_phone_var.get()
        email = self.supplier_email_var.get()
        address = self.supplier_address_var.get()
        
        if not name:
            messagebox.showerror("Error", "Supplier name is required!")
            return
            
        models.add_supplier(name, contact, phone, email, address)
        self.clear_supplier_form()
        self.refresh_suppliers()
        self.status_bar.config(text=f"Supplier '{name}' added successfully!")
        
    def update_supplier(self):
        """Update selected supplier"""
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to update!")
            return
            
        supplier_id = self.suppliers_tree.item(selected[0])['values'][0]
        name = self.supplier_name_var.get()
        contact = self.supplier_contact_var.get()
        phone = self.supplier_phone_var.get()
        email = self.supplier_email_var.get()
        address = self.supplier_address_var.get()
        
        models.update_supplier(supplier_id, name or None, contact or None, phone or None, 
                           email or None, address or None)
        self.clear_supplier_form()
        self.refresh_suppliers()
        self.status_bar.config(text=f"Supplier ID {supplier_id} updated successfully!")
        
    def delete_supplier(self):
        """Delete selected supplier"""
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this supplier?"):
            supplier_id = self.suppliers_tree.item(selected[0])['values'][0]
            models.delete_supplier(supplier_id)
            self.clear_supplier_form()
            self.refresh_suppliers()
            self.status_bar.config(text=f"Supplier ID {supplier_id} deleted successfully!")
            
    def clear_supplier_form(self):
        """Clear supplier form fields"""
        self.supplier_name_var.set("")
        self.supplier_contact_var.set("")
        self.supplier_phone_var.set("")
        self.supplier_email_var.set("")
        self.supplier_address_var.set("")
        
    def refresh_suppliers(self):
        """Refresh suppliers tree view"""
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
            
        suppliers = models.view_suppliers()
        for supplier in suppliers:
            self.suppliers_tree.insert('', 'end', values=supplier)
            
    def on_supplier_double_click(self, event):
        """Handle double click on supplier"""
        selected = self.suppliers_tree.selection()
        if selected:
            supplier = self.suppliers_tree.item(selected[0])['values']
            self.supplier_name_var.set(supplier[1])
            self.supplier_contact_var.set(supplier[2] if supplier[2] else "")
            self.supplier_phone_var.set(supplier[3] if supplier[3] else "")
            self.supplier_email_var.set(supplier[4] if supplier[4] else "")
            self.supplier_address_var.set(supplier[5] if supplier[5] else "")
            
    # ============ Transaction Methods ============
    def add_transaction(self):
        """Add a new transaction"""
        try:
            item_name = self.transaction_item_var.get()
            trans_type = self.transaction_type_var.get()
            quantity = int(self.transaction_quantity_var.get())
            date = self.transaction_date_var.get()
            notes = self.transaction_notes_var.get()
            
            if not item_name or not trans_type:
                messagebox.showerror("Error", "Item and Type are required!")
                return
                
            # Get item ID from name
            items = models.view_items()
            item_id = None
            for item in items:
                if item[1] == item_name:
                    item_id = item[0]
                    break
                    
            if not item_id:
                messagebox.showerror("Error", "Item not found!")
                return
                
            models.add_transaction(item_id, trans_type, quantity, date, notes)
            self.clear_transaction_form()
            self.refresh_transactions()
            self.refresh_inventory()
            self.status_bar.config(text="Transaction added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
            
    def clear_transaction_form(self):
        """Clear transaction form fields"""
        self.transaction_item_var.set("")
        self.transaction_type_var.set("")
        self.transaction_quantity_var.set("")
        self.transaction_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.transaction_notes_var.set("")
        
    def refresh_transactions(self):
        """Refresh transactions tree view"""
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
            
        transactions = models.view_transactions()
        for trans in transactions:
            self.transactions_tree.insert('', 'end', values=(trans[0], trans[6], trans[2], trans[3], trans[4], trans[5] or ""))
            
    def update_categories_combo(self):
        """Update categories dropdown list"""
        categories = models.view_categories()
        category_names = [cat[1] for cat in categories]
        self.category_combo['values'] = category_names
        
    def update_items_combo(self):
        """Update items dropdown list"""
        items = models.view_items()
        item_names = [item[1] for item in items]
        self.transaction_item_combo['values'] = item_names
        
    def clear_all_data(self):
        """Clear all data from database with confirmation"""
        # First confirmation
        if not messagebox.askyesno("Confirm Clear Data", 
                                  "⚠️ WARNING: This will delete ALL data including:\n\n"
                                  "• All inventory items\n"
                                  "• All categories\n"
                                  "• All suppliers\n"
                                  "• All transactions\n"
                                  "• All users (except you will be logged out)\n\n"
                                  "This action cannot be undone!\n\n"
                                  "Do you want to continue?"):
            return
            
        # Second confirmation with password
        password = messagebox.askstring("Final Confirmation", 
                                       "Please type 'DELETE' to confirm permanent data deletion:")
        if password != "DELETE":
            messagebox.showerror("Cancelled", "Data deletion cancelled.")
            return
            
        try:
            # Clear all data
            models.clear_all_data()
            
            # Show success message
            messagebox.showinfo("Success", "All data has been cleared successfully!\n\n"
                                             "The application will now exit.\n"
                                             "Please restart to create a fresh database.")
            
            # Logout and exit
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear data: {str(e)}")
