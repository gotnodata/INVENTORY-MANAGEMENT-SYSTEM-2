import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime
import main

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Login frame
        login_frame = ttk.Frame(root, padding="20")
        login_frame.pack(expand=True)
        
        # Title
        title_label = ttk.Label(login_frame, text="Inventory Management System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Username
        ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var, width=20)
        username_entry.grid(row=1, column=1, pady=5)
        username_entry.focus()
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, 
                                  show="*", width=20)
        password_entry.grid(row=2, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=root.quit).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to login
        root.bind('<Return>', lambda event: self.login())
        
        self.authenticated_user = None
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
            
        user = main.authenticate_user(username, password)
        if user:
            self.authenticated_user = user
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
            self.password_var.set("")
            self.username_var.focus()

class InventoryManagementGUI:
    def __init__(self, root, user):
        self.root = root
        self.current_user = user
        self.root.title(f"Inventory Management System - {user['username']} ({user['role']})")
        self.root.geometry("1200x700")
        
        # Initialize database
        main.init_db()
        main.create_categories_table()
        main.create_suppliers_table()
        main.create_transactions_table()
        main.create_users_table()
        
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
        if user['role'] == 'admin':
            self.create_users_tab()
        
        # Status bar
        self.status_bar = tk.Label(root, text=f"Logged in as: {user['username']} ({user['role']})", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # User menu (admin only)
        if self.current_user['role'] == 'admin':
            user_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Users", menu=user_menu)
            user_menu.add_command(label="Add User", command=self.show_add_user_dialog)
            user_menu.add_command(label="View Users", command=self.view_users_dialog)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            self.show_login()
            
    def show_login(self):
        root = tk.Tk()
        login_window = LoginWindow(root)
        root.mainloop()
        
        if login_window.authenticated_user:
            new_root = tk.Tk()
            app = InventoryManagementGUI(new_root, login_window.authenticated_user)
            new_root.mainloop()
            
    def show_about(self):
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
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(expand=True)
        
        # Form fields
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=username_var, width=25).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=password_var, show="*", width=25).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=email_var, width=25).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Role:").grid(row=3, column=0, sticky=tk.W, pady=5)
        role_var = tk.StringVar(value="user")
        role_combo = ttk.Combobox(frame, textvariable=role_var, values=["user", "admin"], width=23)
        role_combo.grid(row=3, column=1, pady=5)
        
        def create_user():
            username = username_var.get().strip()
            password = password_var.get()
            email = email_var.get().strip() or None
            role = role_var.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Username and password are required!")
                return
                
            if len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters!")
                return
                
            if main.create_user(username, password, email, role):
                messagebox.showinfo("Success", f"User '{username}' created successfully!")
                dialog.destroy()
                if hasattr(self, 'users_tree'):
                    self.refresh_users()
            else:
                messagebox.showerror("Error", "Failed to create user (username may already exist)!")
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Create User", command=create_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def view_users_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Users")
        dialog.geometry("600x400")
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Users", font=("Arial", 12, "bold")).pack(pady=5)
        
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
        
    def refresh_users(self):
        if hasattr(self, 'users_tree'):
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
                
            users = main.get_all_users()
            for user in users:
                self.users_tree.insert('', 'end', values=user)
                
    def create_users_tab(self):
        # Users Tab (Admin only)
        self.users_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.users_frame, text="Users")
        
        # Button frame
        button_frame = ttk.Frame(self.users_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add User", command=self.show_add_user_dialog).pack(side=tk.LEFT, padx=5)
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
        # Inventory Tab
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="Inventory")
        
        # Left panel for form
        left_frame = ttk.Frame(self.inventory_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Form fields
        ttk.Label(left_frame, text="Inventory Management", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
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
        
        ttk.Label(right_frame, text="Inventory Items", font=("Arial", 12, "bold")).pack(pady=5)
        
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
        ttk.Button(search_frame, text="Refresh", command=self.refresh_inventory).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.refresh_inventory()
        self.update_categories_combo()
        
    def create_categories_tab(self):
        # Categories Tab
        self.categories_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.categories_frame, text="Categories")
        
        # Left panel for form
        left_frame = ttk.Frame(self.categories_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Category Management", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
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
        
        ttk.Label(right_frame, text="Categories", font=("Arial", 12, "bold")).pack(pady=5)
        
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
        # Suppliers Tab
        self.suppliers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.suppliers_frame, text="Suppliers")
        
        # Left panel for form
        left_frame = ttk.Frame(self.suppliers_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Supplier Management", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
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
        
        ttk.Label(right_frame, text="Suppliers", font=("Arial", 12, "bold")).pack(pady=5)
        
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
        # Transactions Tab
        self.transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.transactions_frame, text="Transactions")
        
        # Left panel for form
        left_frame = ttk.Frame(self.transactions_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Transaction Management", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(left_frame, text="Item:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.transaction_item_var = tk.StringVar()
        self.transaction_item_combo = ttk.Combobox(left_frame, textvariable=self.transaction_item_var, width=28)
        self.transaction_item_combo.grid(row=1, column=1, pady=5)
        
        ttk.Label(left_frame, text="Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.transaction_type_var = tk.StringVar()
        type_combo = ttk.Combobox(left_frame, textvariable=self.transaction_type_var, width=28, values=['IN', 'OUT'])
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
        
        ttk.Label(right_frame, text="Transactions", font=("Arial", 12, "bold")).pack(pady=5)
        
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
        
    # Inventory methods
    def add_item(self):
        try:
            name = self.item_name_var.get()
            category = self.item_category_var.get()
            quantity = int(self.item_quantity_var.get())
            price = float(self.item_price_var.get())
            
            if not name or not category:
                messagebox.showerror("Error", "Name and Category are required!")
                return
            
            main.add_item(name, category, quantity, price)
            self.clear_inventory_form()
            self.refresh_inventory()
            self.status_bar.config(text=f"Item '{name}' added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price!")
            
    def update_item(self):
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
            
            # Convert to appropriate types or None
            quantity = int(quantity) if quantity else None
            price = float(price) if price else None
            name = name if name else None
            category = category if category else None
            
            main.update_item(item_id, name, category, quantity, price)
            self.clear_inventory_form()
            self.refresh_inventory()
            self.status_bar.config(text=f"Item ID {item_id} updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price!")
            
    def delete_item(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            item_id = self.inventory_tree.item(selected[0])['values'][0]
            main.delete_item(item_id)
            self.clear_inventory_form()
            self.refresh_inventory()
            self.status_bar.config(text=f"Item ID {item_id} deleted successfully!")
            
    def clear_inventory_form(self):
        self.item_name_var.set("")
        self.item_category_var.set("")
        self.item_quantity_var.set("")
        self.item_price_var.set("")
        
    def refresh_inventory(self):
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        # Add items
        items = main.view_items()
        for item in items:
            self.inventory_tree.insert('', 'end', values=item)
            
    def search_inventory(self):
        search_term = self.search_var.get().lower()
        if not search_term:
            self.refresh_inventory()
            return
            
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        # Add filtered items
        items = main.view_items()
        for item in items:
            if (search_term in str(item[1]).lower() or 
                search_term in str(item[2]).lower()):
                self.inventory_tree.insert('', 'end', values=item)
                
    def on_inventory_double_click(self, event):
        selected = self.inventory_tree.selection()
        if selected:
            item = self.inventory_tree.item(selected[0])['values']
            self.item_name_var.set(item[1])
            self.item_category_var.set(item[2])
            self.item_quantity_var.set(item[3])
            self.item_price_var.set(item[4])
            
    # Category methods
    def add_category(self):
        name = self.category_name_var.get()
        description = self.category_desc_var.get()
        
        if not name:
            messagebox.showerror("Error", "Category name is required!")
            return
            
        main.add_category(name, description)
        self.clear_category_form()
        self.refresh_categories()
        self.update_categories_combo()
        self.status_bar.config(text=f"Category '{name}' added successfully!")
        
    def update_category(self):
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to update!")
            return
            
        category_id = self.categories_tree.item(selected[0])['values'][0]
        name = self.category_name_var.get()
        description = self.category_desc_var.get()
        
        name = name if name else None
        description = description if description else None
        
        main.update_category(category_id, name, description)
        self.clear_category_form()
        self.refresh_categories()
        self.update_categories_combo()
        self.status_bar.config(text=f"Category ID {category_id} updated successfully!")
        
    def delete_category(self):
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?"):
            category_id = self.categories_tree.item(selected[0])['values'][0]
            main.delete_category(category_id)
            self.clear_category_form()
            self.refresh_categories()
            self.update_categories_combo()
            self.status_bar.config(text=f"Category ID {category_id} deleted successfully!")
            
    def clear_category_form(self):
        self.category_name_var.set("")
        self.category_desc_var.set("")
        
    def refresh_categories(self):
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
            
        categories = main.view_categories()
        for category in categories:
            self.categories_tree.insert('', 'end', values=category)
            
    def on_category_double_click(self, event):
        selected = self.categories_tree.selection()
        if selected:
            category = self.categories_tree.item(selected[0])['values']
            self.category_name_var.set(category[1])
            self.category_desc_var.set(category[2] if category[2] else "")
            
    # Supplier methods
    def add_supplier(self):
        name = self.supplier_name_var.get()
        contact = self.supplier_contact_var.get()
        phone = self.supplier_phone_var.get()
        email = self.supplier_email_var.get()
        address = self.supplier_address_var.get()
        
        if not name:
            messagebox.showerror("Error", "Supplier name is required!")
            return
            
        main.add_supplier(name, contact, phone, email, address)
        self.clear_supplier_form()
        self.refresh_suppliers()
        self.status_bar.config(text=f"Supplier '{name}' added successfully!")
        
    def update_supplier(self):
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
        
        main.update_supplier(supplier_id, name or None, contact or None, phone or None, 
                           email or None, address or None)
        self.clear_supplier_form()
        self.refresh_suppliers()
        self.status_bar.config(text=f"Supplier ID {supplier_id} updated successfully!")
        
    def delete_supplier(self):
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this supplier?"):
            supplier_id = self.suppliers_tree.item(selected[0])['values'][0]
            main.delete_supplier(supplier_id)
            self.clear_supplier_form()
            self.refresh_suppliers()
            self.status_bar.config(text=f"Supplier ID {supplier_id} deleted successfully!")
            
    def clear_supplier_form(self):
        self.supplier_name_var.set("")
        self.supplier_contact_var.set("")
        self.supplier_phone_var.set("")
        self.supplier_email_var.set("")
        self.supplier_address_var.set("")
        
    def refresh_suppliers(self):
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
            
        suppliers = main.view_suppliers()
        for supplier in suppliers:
            self.suppliers_tree.insert('', 'end', values=supplier)
            
    def on_supplier_double_click(self, event):
        selected = self.suppliers_tree.selection()
        if selected:
            supplier = self.suppliers_tree.item(selected[0])['values']
            self.supplier_name_var.set(supplier[1])
            self.supplier_contact_var.set(supplier[2] if supplier[2] else "")
            self.supplier_phone_var.set(supplier[3] if supplier[3] else "")
            self.supplier_email_var.set(supplier[4] if supplier[4] else "")
            self.supplier_address_var.set(supplier[5] if supplier[5] else "")
            
    # Transaction methods
    def add_transaction(self):
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
            items = main.view_items()
            item_id = None
            for item in items:
                if item[1] == item_name:
                    item_id = item[0]
                    break
                    
            if not item_id:
                messagebox.showerror("Error", "Item not found!")
                return
                
            main.add_transaction(item_id, trans_type, quantity, date, notes)
            self.clear_transaction_form()
            self.refresh_transactions()
            self.refresh_inventory()  # Update inventory to reflect quantity changes
            self.status_bar.config(text="Transaction added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
            
    def clear_transaction_form(self):
        self.transaction_item_var.set("")
        self.transaction_type_var.set("")
        self.transaction_quantity_var.set("")
        self.transaction_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.transaction_notes_var.set("")
        
    def refresh_transactions(self):
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
            
        transactions = main.view_transactions()
        for trans in transactions:
            self.transactions_tree.insert('', 'end', values=(trans[0], trans[6], trans[2], trans[3], trans[4], trans[5] or ""))
            
    def update_categories_combo(self):
        categories = main.view_categories()
        category_names = [cat[1] for cat in categories]
        self.category_combo['values'] = category_names
        
    def update_items_combo(self):
        items = main.view_items()
        item_names = [item[1] for item in items]
        self.transaction_item_combo['values'] = item_names

if __name__ == "__main__":
    # Initialize database and create admin user if needed
    main.init_db()
    main.create_categories_table()
    main.create_suppliers_table()
    main.create_transactions_table()
    main.create_users_table()
    
    # Check if any users exist
    users = main.get_all_users()
    if not users:
        # Create first admin user
        setup_root = tk.Tk()
        setup_root.withdraw()  # Hide the main window
        
        username = simpledialog.askstring("First Time Setup", "Enter admin username:")
        if username:
            password = simpledialog.askstring("First Time Setup", "Enter admin password:", show='*')
            if password and len(password) >= 4:
                email = simpledialog.askstring("First Time Setup", "Enter admin email (optional):")
                if main.create_user(username, password, email, 'admin'):
                    messagebox.showinfo("Success", f"Admin user '{username}' created successfully!")
                else:
                    messagebox.showerror("Error", "Failed to create admin user!")
        
        setup_root.destroy()
    
    # Show login window
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
    
    # If login successful, show main application
    if login_window.authenticated_user:
        main_root = tk.Tk()
        app = InventoryManagementGUI(main_root, login_window.authenticated_user)
        main_root.mainloop()
