"""Main application window for Inventory Management System"""
import tkinter as tk
from tkinter import ttk, messagebox
import config
from ui.menu import MenuManager
from ui.tabs.inventory_tab import InventoryTab
from ui.tabs.categories_tab import CategoriesTab
from ui.tabs.suppliers_tab import SuppliersTab
from ui.tabs.transactions_tab import TransactionsTab
from ui.tabs.users_tab import UsersTab
from ui.tabs.reports_tab import ReportsTab


class InventoryManagementGUI:
    """Main application window class - coordinates all tabs"""
    
    def __init__(self, root, user):
        """
        Initialize the main GUI
        
        Args:
            root: tk.Tk root window
            user: Dictionary with user info {id, username, email, role, created_at}
        """
        self.root = root
        self.current_user = user
        
        # Setup window
        self.root.iconbitmap("ui/images/favicon.ico")
        self.root.title(f"{config.MAIN_WINDOW_TITLE} - {user['username']} ({user['role']})")
        self.root.geometry(config.MAIN_WINDOW_GEOMETRY)
        
        # Create menu bar
        MenuManager(self.root, on_logout=self._logout, on_about=self._show_about)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create status bar
        self.status_bar = tk.Label(
            self.root, 
            text=f"Logged in as: {user['username']} ({user['role']})", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create tabs
        self._create_tabs(user)
    
    def _create_tabs(self, user):
        """Create all application tabs based on user role"""
        # Standard tabs available to all users
        InventoryTab(self.notebook, self._update_status)
        CategoriesTab(self.notebook, self._update_status)
        SuppliersTab(self.notebook, self._update_status)
        TransactionsTab(self.notebook, self._update_status)
        
        # Admin-only tabs
        if user['role'] == config.ROLE_ADMIN:
            UsersTab(self.notebook, self._update_status)
            ReportsTab(self.notebook, self._update_status)
    
    def _update_status(self, message):
        """Update status bar message
        
        Args:
            message: Status message to display
        """
        self.status_bar.config(text=message)
    
    def _logout(self):
        """Handle logout"""
        self.root.destroy()
    
    @staticmethod
    def _show_about():
        """Show about dialog"""
        about_text = """Inventory Management System v2.0
        
Features:
• Inventory Management
• Category Management  
• Supplier Management
• Transaction Tracking
• User Authentication
• Role-based Access Control

"""
        messagebox.showinfo("About", about_text)
        
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

"""
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
        dialog.iconbitmap("ui/images/favicon.ico")
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
        
        ttk.Label(left_frame, text="Cost Price:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.item_cost_price_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.item_cost_price_var, width=30).grid(row=4, column=1, pady=5)
        
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
        columns = ('ID', 'Name', 'Category', 'Quantity', 'Cost Price')
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

        # Use grid so the Refresh button doesn't get clipped
        search_frame.columnconfigure(1, weight=1)  # allow the entry to expand

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)

        ttk.Button(search_frame, text="Search", command=self.search_inventory).grid(
            row=0, column=2, sticky=tk.E, padx=5
        )
        ttk.Button(search_frame, text="Refresh", command=self.refresh_inventory).grid(
            row=0, column=3, sticky=tk.E, padx=5
        )
        
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
        self.transaction_item_combo.bind('<<ComboboxSelected>>', self.on_transaction_item_selected)
        
        
        
        ttk.Label(left_frame, text="Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.transaction_type_var = tk.StringVar()
        type_combo = ttk.Combobox(left_frame, textvariable=self.transaction_type_var, width=28, 
                                 values=[config.TRANSACTION_TYPE_IN, config.TRANSACTION_TYPE_OUT])
        type_combo.grid(row=3, column=1, pady=5)
        type_combo.bind('<<ComboboxSelected>>', self.on_transaction_type_changed)
        
        ttk.Label(left_frame, text="Quantity:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.transaction_quantity_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.transaction_quantity_var, width=30).grid(row=4, column=1, pady=5)
        
        ttk.Label(left_frame, text="Date:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.transaction_date_var = tk.StringVar()
        self.transaction_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(left_frame, textvariable=self.transaction_date_var, width=30).grid(row=5, column=1, pady=5)
        
        ttk.Label(left_frame, text="Selling Price:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.transaction_selling_price_var = tk.StringVar()
        self.transaction_selling_price_entry = ttk.Entry(left_frame, textvariable=self.transaction_selling_price_var, width=30)
        self.transaction_selling_price_entry.grid(row=6, column=1, pady=5)
        
        ttk.Label(left_frame, text="Notes:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.transaction_notes_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.transaction_notes_var, width=30).grid(row=7, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
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
            category_name = self.item_category_var.get()
            quantity = int(self.item_quantity_var.get())
            cost_price = float(self.item_cost_price_var.get()) if self.item_cost_price_var.get() else 0.0
            
            if not name or not category_name:
                messagebox.showerror("Error", "Name and Category are required!")
                return
                
            # Get category ID
            categories = models.get_categories()
            category_id = None
            for cat in categories:
                if cat[1] == category_name:
                    category_id = cat[0]
                    break
                    
            if not category_id:
                messagebox.showerror("Error", "Category not found!")
                return
            
            models.add_item(name, category_id, quantity, cost_price)
            
            self.clear_inventory_form()
            self.refresh_inventory()
            self.status_bar.config(text=f"Item '{name}' added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid quantity or price format! {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")
            
    def update_item(self):
        """Update selected inventory item"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to update!")
            return
            
        try:
            item_id = self.inventory_tree.item(selected[0])['values'][0]
            name = self.item_name_var.get()
            category_name = self.item_category_var.get()
            quantity = self.item_quantity_var.get()
            cost_price = self.item_cost_price_var.get()
            
            # Handle empty strings vs None values
            name = name if name.strip() else None
            category_id = None
            quantity = int(quantity) if quantity else None
            cost_price = float(cost_price) if cost_price else None
            
            # Get category ID from name
            if category_name:
                categories = models.view_categories()
                for cat in categories:
                    if cat[1] == category_name:
                        category_id = cat[0]
                        break
            
            models.update_item(item_id, name, category_id, quantity, cost_price)
            self.clear_inventory_form()
            self.refresh_inventory()
            self.status_bar.config(text=f"Item ID {item_id} updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid quantity or price! {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {e}")
            
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
        """Clear all inventory form fields"""
        self.item_name_var.set("")
        self.item_category_var.set("")
        self.item_quantity_var.set("")
        self.item_cost_price_var.set("")
        
    def refresh_inventory(self):
        """Refresh inventory tree view with measurement units"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        items = models.view_items()
        for item in items:
            # Data structure from SELECT i.*, c.name as category_name, mu.unit_name, mu.unit_symbol:
            # inventory i.* columns are: [id, name, category_id, quantity, price, measurement_unit_id, cost_price]
            # then we add: [category_name, unit_name, unit_symbol]
            # Final order:
            # [id, name, category_id, quantity, price, measurement_unit_id, cost_price, category_name, unit_name, unit_symbol]
            
            # Extract values with correct indices
            item_id = item[0]
            item_name = item[1]
            cost_price = item[6] if len(item) > 6 and item[6] is not None else 0.0  # cost_price at index 6
            category_name = item[7] if len(item) > 7 and item[7] else "No Category"  # category_name at index 7
            quantity = item[3]
            unit_symbol = item[9] if len(item) > 9 and item[9] else ""  # unit_symbol at index 9
            
            # Create display values: [id, name, category_name, quantity_with_unit, cost_price]
            display_values = [
                item_id,  # ID
                item_name,  # Name
                category_name,  # Category name
                f"{quantity} {unit_symbol}" if unit_symbol else str(quantity),  # Quantity with unit
                cost_price  # Cost Price
            ]
            self.inventory_tree.insert('', 'end', values=display_values)
            
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
            # Final order from models.view_items():
            # [id, name, category_id, quantity, price, measurement_unit_id, cost_price, category_name, unit_name, unit_symbol]
            
            # Extract values with correct indices
            item_id = item[0]
            item_name = item[1]
            cost_price = item[6] if len(item) > 6 and item[6] is not None else 0.0
            category_name = item[7] if len(item) > 7 and item[7] else "No Category"
            quantity = item[3]
            unit_symbol = item[9] if len(item) > 9 and item[9] else ""
            
            # Create display values: [id, name, category_name, quantity_with_unit, cost_price]
            display_values = [
                item_id,  # ID
                item_name,  # Name
                category_name,  # Category name
                f"{quantity} {unit_symbol}" if unit_symbol else str(quantity),  # Quantity with unit
                cost_price  # Cost Price
            ]
            
            # Check if item matches search term
            if (search_term in str(item_name).lower() or 
                search_term in str(category_name).lower()):
                self.inventory_tree.insert('', 'end', values=display_values)
                
    def on_inventory_double_click(self, event):
        """Handle double click on inventory item"""
        selected = self.inventory_tree.selection()
        if selected:
            item = self.inventory_tree.item(selected[0])['values']
            self.item_name_var.set(item[1])  # Name
            self.item_category_var.set(item[2])  # Category name
            
            # Extract quantity from "10 pcs" format - just get the number
            quantity_str = str(item[3])
            quantity_parts = quantity_str.split()
            self.item_quantity_var.set(quantity_parts[0])  # Just the number part
            
            self.item_cost_price_var.set(item[4])  # Cost price
            
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
            
        categories = models.get_categories()
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
            
        suppliers = models.get_suppliers()
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
            selling_price = float(self.transaction_selling_price_var.get()) if self.transaction_selling_price_var.get() else None
            
            if not item_name or not trans_type:
                messagebox.showerror("Error", "Item and Type are required!")
                return
                
            # Get item ID from name
            # Get item data
            items = models.view_items()
            item_id = None
            item_data = None
            for item in items:
                if item[1] == item_name:
                    item_id = item[0]
                    item_data = item
                    break
                    
            if not item_id:
                messagebox.showerror("Error", "Item not found!")
                return
            
            # Check for OUT transaction with insufficient quantity
            if trans_type == config.TRANSACTION_TYPE_OUT:
                current_quantity = item_data[3]  # quantity is at index 3
                if quantity > current_quantity:
                    messagebox.showerror("Error", 
                        f"Insufficient inventory!\n"
                        f"Current quantity: {current_quantity}\n"
                        f"Attempted to sell: {quantity}")
                    return
                
            # Add transaction (this will automatically update inventory)
            success, message = models.add_transaction(item_id, trans_type, quantity, date, notes, selling_price)
            
            if success:
                self.clear_transaction_form()
                self.refresh_transactions()
                self.refresh_inventory()
                
                # Update current quantity display if item is still selected
                if self.transaction_item_var.get() == item_name:
                    pass  # Current quantity display removed
                
                self.status_bar.config(text=f"Transaction added successfully! {message}")
            else:
                messagebox.showerror("Error", message)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid quantity! {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaction: {e}")
            
    def on_transaction_item_selected(self, event):
        """Handle item selection in transaction form"""
        item_name = self.transaction_item_var.get()
        # Current quantity display functionality removed to avoid undefined label errors
            
    def clear_transaction_form(self):
        """Clear transaction form fields"""
        self.transaction_item_var.set("")
        self.transaction_type_var.set("")
        self.transaction_quantity_var.set("")
        self.transaction_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.transaction_selling_price_var.set("")
        self.transaction_notes_var.set("")
        # Enable selling price field by default
        self.transaction_selling_price_entry.config(state='normal')
        
    def on_transaction_type_changed(self, event):
        """Handle transaction type change to enable/disable selling price field"""
        trans_type = self.transaction_type_var.get()
        if trans_type == config.TRANSACTION_TYPE_IN:
            # Disable selling price for IN transactions
            self.transaction_selling_price_entry.config(state='disabled')
            self.transaction_selling_price_var.set("")
        else:
            # Enable selling price for OUT transactions
            self.transaction_selling_price_entry.config(state='normal')
        
    def refresh_transactions(self):
        """Refresh transactions tree view with measurement units"""
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
            
        transactions = models.get_transactions()
        for trans in transactions:
            # trans[0]=id, trans[1]=item_id, trans[2]=type, trans[3]=quantity, trans[4]=date, trans[5]=notes, trans[6]=item_name, trans[7]=unit_symbol, trans[8]=unit_name
            # Format quantity with unit if available
            quantity_display = str(trans[3])
            if trans[7]:  # unit_symbol exists
                quantity_display += f" {trans[7]}"
            elif trans[8]:  # unit_name exists
                quantity_display += f" {trans[8]}"
            
            # Display: ID, Item Name, Type, Quantity with units, Date, Notes
            self.transactions_tree.insert('', 'end', values=(trans[0], trans[6], trans[2], quantity_display, trans[4], trans[5] or ""))


    def update_categories_combo(self):
        """Update categories dropdown list"""
        categories = models.get_categories()
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

    def create_reports_tab(self):
        """Create the reports management tab for admins"""
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="Reports")
        
        # Main container
        main_container = ttk.Frame(self.reports_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Report generation
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Generate Reports", font=config.DEFAULT_FONT_LABEL).pack(pady=10)
        
        # Report type selection
        ttk.Label(left_frame, text="Report Type:").pack(anchor=tk.W, pady=5)
        self.report_type_var = tk.StringVar()
        report_types = [
            "Inventory Report",
            "Transaction Report", 
            "Sales Report",
            "Profit & Loss Report",
            "User Activity Report",
            "Supplier Report"
        ]
        self.report_type_combo = ttk.Combobox(left_frame, textvariable=self.report_type_var, 
                                             values=report_types, width=30, state="readonly")
        self.report_type_combo.pack(pady=5)
        self.report_type_combo.current(0)
        
        # Date filtering for transaction/sales reports
        ttk.Label(left_frame, text="Date Range (Optional):").pack(anchor=tk.W, pady=(20, 5))
        
        date_frame = ttk.Frame(left_frame)
        date_frame.pack(pady=5)
        
        ttk.Label(date_frame, text="From:").grid(row=0, column=0, padx=5)
        self.start_date_var = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.start_date_var, width=12).grid(row=0, column=1, padx=5)
        
        ttk.Label(date_frame, text="To:").grid(row=0, column=2, padx=5)
        self.end_date_var = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.end_date_var, width=12).grid(row=0, column=3, padx=5)
        
        # Set default dates (last 30 days)
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        self.start_date_var.set(start_date)
        self.end_date_var.set(end_date)
        
        # Generate button
        ttk.Button(left_frame, text="Generate Report", 
                  command=self.generate_report).pack(pady=20)
        
        # Export buttons
        ttk.Label(left_frame, text="Export Options:").pack(anchor=tk.W, pady=(20, 5))
        
        export_frame = ttk.Frame(left_frame)
        export_frame.pack(pady=5)
        
        ttk.Button(export_frame, text="Export to CSV", 
                  command=lambda: self.export_report('csv')).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Export to TXT", 
                  command=lambda: self.export_report('txt')).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Report display
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Report Preview", font=config.DEFAULT_FONT_LABEL).pack(pady=5)
        
        # Report text widget with scrollbar
        report_container = ttk.Frame(right_frame)
        report_container.pack(fill=tk.BOTH, expand=True)
        
        self.report_text = tk.Text(report_container, wrap=tk.WORD, width=80, height=30)
        scrollbar = ttk.Scrollbar(report_container, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status label
        self.report_status_var = tk.StringVar()
        self.report_status_var.set("Select a report type and click Generate")
        
        # Create a more prominent status bar at the bottom of the window
        status_container = ttk.Frame(right_frame)
        status_container.pack(side=tk.BOTTOM, fill=tk.X, pady=5, padx=10)
        
        # Add a separator line for visual separation
        separator = ttk.Separator(status_container, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 5))
        
        # Create a frame for the status message
        status_frame = ttk.Frame(status_container)
        status_frame.pack(fill=tk.X)
        
        # Create a highly visible status label with enhanced styling
        self.status_label = ttk.Label(status_frame, textvariable=self.report_status_var, 
                                     font=('Arial', 12, 'bold'), 
                                     foreground='green', 
                                     background='lightgray',
                                     relief='raised', 
                                     borderwidth=2,
                                     padding=(10, 5))
        self.status_label.pack(fill=tk.X, expand=True)
        
        # Store current report data
        self.current_report_data = None

    def set_report_status(self, message, status_type='success'):
        """Update report status with appropriate styling"""
        self.report_status_var.set(message)
        
        # Update label styling based on status type
        if status_type == 'success':
            self.status_label.configure(foreground='white', background='green', 
                                     font=('Arial', 12, 'bold'))
        elif status_type == 'error':
            self.status_label.configure(foreground='white', background='red', 
                                     font=('Arial', 12, 'bold'))
        elif status_type == 'info':
            self.status_label.configure(foreground='white', background='blue', 
                                     font=('Arial', 12, 'normal'))
        else:  # processing
            self.status_label.configure(foreground='black', background='yellow', 
                                     font=('Arial', 12, 'normal'))

    def generate_report(self):
        """Generate the selected report"""
        report_type = self.report_type_var.get()
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        if not report_type:
            messagebox.showerror("Error", "Please select a report type!")
            return
        
        try:
            self.set_report_status("Generating report...", 'processing')
            self.report_text.delete(1.0, tk.END)
            
            # Generate the appropriate report
            if report_type == "Inventory Report":
                self.current_report_data = models.generate_inventory_report()
                self._display_inventory_report()
            elif report_type == "Transaction Report":
                self.current_report_data = models.generate_transaction_report(start_date, end_date)
                self._display_transaction_report()
            elif report_type == "Sales Report":
                self.current_report_data = models.generate_sales_report(start_date, end_date)
                self._display_sales_report()
            elif report_type == "Profit & Loss Report":
                self.current_report_data = models.generate_profit_loss_report(start_date, end_date)
                self._display_profit_loss_report()
            elif report_type == "User Activity Report":
                self.current_report_data = models.generate_user_activity_report()
                self._display_user_activity_report()
            elif report_type == "Supplier Report":
                self.current_report_data = models.generate_supplier_report()
                self._display_supplier_report()
            
            self.set_report_status(f"✅ Report generated successfully! ({self.current_report_data['generated_at']})", 'success')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.set_report_status("❌ Error generating report", 'error')

    def _display_inventory_report(self):
        """Display inventory report in text widget"""
        data = self.current_report_data
        
        # Header
        self.report_text.insert(tk.END, "=" * 80 + "\n")
        self.report_text.insert(tk.END, "INVENTORY REPORT\n")
        self.report_text.insert(tk.END, "=" * 80 + "\n\n")
        self.report_text.insert(tk.END, f"Generated: {data['generated_at']}\n\n")
        
        # Summary
        self.report_text.insert(tk.END, "SUMMARY\n")
        self.report_text.insert(tk.END, "-" * 40 + "\n")
        self.report_text.insert(tk.END, f"Total Items: {data['summary']['total_items']}\n")
        self.report_text.insert(tk.END, f"Total Quantity: {data['summary']['total_quantity']}\n")
        self.report_text.insert(tk.END, f"Total Value: ${data['summary']['total_value']:.2f}\n\n")
        
        # Items
        self.report_text.insert(tk.END, "INVENTORY ITEMS\n")
        self.report_text.insert(tk.END, "-" * 40 + "\n")
        self.report_text.insert(tk.END, f"{'ID':<5} {'Name':<25} {'Category':<15} {'Qty':<10} {'Cost':<10} {'Value':<10} {'Status':<12}\n")
        self.report_text.insert(tk.END, "-" * 80 + "\n")
        for item in data['items']:
            self.report_text.insert(tk.END, 
                f"{item[0]:<5} {item[1]:<25} {item[2]:<15} {item[3]:<10} ${item[4]:<9.2f} ${item[5]:<9.2f} {item[7]:<12}\n")
        
        # Low stock
        if data['low_stock']:
            self.report_text.insert(tk.END, "\nLOW STOCK ITEMS\n")
            self.report_text.insert(tk.END, "-" * 40 + "\n")
            for item in data['low_stock']:
                self.report_text.insert(tk.END, f"{item[0]}: {item[1]} {item[2] or 'units'}\n")
        
        # Out of stock
        if data['out_of_stock']:
            self.report_text.insert(tk.END, "\nOUT OF STOCK ITEMS\n")
            self.report_text.insert(tk.END, "-" * 40 + "\n")
            for item in data['out_of_stock']:
                self.report_text.insert(tk.END, f"{item[0]} ({item[1]})\n")

    def _display_transaction_report(self):
        """Display transaction report in text widget"""
        data = self.current_report_data
        
        # Debug: Check if data exists
        if not data or 'transactions' not in data:
            self.report_text.insert(tk.END, "No transaction data available.\n")
            return
        
        # Header
        self.report_text.insert(tk.END, "=" * 80 + "\n")
        self.report_text.insert(tk.END, "TRANSACTION REPORT\n")
        self.report_text.insert(tk.END, "=" * 80 + "\n\n")
        self.report_text.insert(tk.END, f"Generated: {data['generated_at']}\n")
        self.report_text.insert(tk.END, f"Period: {data['filter_period']}\n\n")
        
        # Summary
        self.report_text.insert(tk.END, "SUMMARY\n")
        self.report_text.insert(tk.END, "-" * 40 + "\n")
        if data.get('summary'):
            for summary in data['summary']:
                self.report_text.insert(tk.END, 
                    f"{summary[0].title()}: {summary[1]} transactions, "
                    f"Total quantity: {summary[2]}, Total value: ${summary[3]:.2f}\n")
        else:
            self.report_text.insert(tk.END, "No summary data available.\n")
        self.report_text.insert(tk.END, "\n")
        
        # Recent transactions (show first 50)
        self.report_text.insert(tk.END, "RECENT TRANSACTIONS (First 50)\n")
        self.report_text.insert(tk.END, "-" * 40 + "\n")
        self.report_text.insert(tk.END, f"{'ID':<5} {'Date':<12} {'Type':<8} {'Item':<20} {'Qty':<8} {'Unit':<6} {'Value':<10}\n")
        self.report_text.insert(tk.END, "-" * 80 + "\n")
        
        if data.get('transactions'):
            for i, trans in enumerate(data['transactions'][:50]):
                try:
                    # Safely access transaction data with proper indexing
                    trans_id = trans[0] if len(trans) > 0 else 'N/A'
                    trans_date = trans[1] if len(trans) > 1 else 'N/A'
                    trans_type = trans[2] if len(trans) > 2 else 'N/A'
                    quantity = trans[3] if len(trans) > 3 else 'N/A'
                    notes = trans[4] if len(trans) > 4 else ''
                    item_name = trans[5] if len(trans) > 5 else 'N/A'
                    category = trans[6] if len(trans) > 6 else 'N/A'
                    unit_symbol = trans[7] if len(trans) > 7 else 'N/A'
                    value = trans[8] if len(trans) > 8 else 0.0
                    
                    self.report_text.insert(tk.END, 
                        f"{trans_id:<5} {trans_date:<12} {trans_type:<8} {item_name:<20} {quantity:<8} {unit_symbol:<6} ${value:<9.2f}\n")
                except Exception as e:
                    self.report_text.insert(tk.END, f"Error displaying transaction {i}: {str(e)}\n")
        else:
            self.report_text.insert(tk.END, "No transaction data available.\n")


    def _display_sales_report(self):
        """Display sales report in text widget"""
        data = self.current_report_data
        
        # Header
        self.report_text.insert(tk.END, "=" * 80 + "\n")
        self.report_text.insert(tk.END, "SALES REPORT\n")
        self.report_text.insert(tk.END, "=" * 80 + "\n\n")
        self.report_text.insert(tk.END, f"Generated: {data['generated_at']}\n")
        self.report_text.insert(tk.END, f"Period: {data['filter_period']}\n\n")
        
        # Top items by revenue
        self.report_text.insert(tk.END, "TOP ITEMS BY REVENUE\n")
        self.report_text.insert(tk.END, "-" * 40 + "\n")
        self.report_text.insert(tk.END, f"{'Item':<25} {'Category':<15} {'Sales':<8} {'Revenue':<12}\n")
        self.report_text.insert(tk.END, "-" * 60 + "\n")
        
        for item in data['item_summary'][:20]:  # Top 20 items
            self.report_text.insert(tk.END, 
                f"{item[0]:<25} {item[1]:<15} {item[2]:<8} ${item[4]:<11.2f}\n")

    def _display_user_activity_report(self):
        """Display user activity report in text widget"""
        data = self.current_report_data
        
        # Header
        self.report_text.insert(tk.END, "=" * 80 + "\n")
        self.report_text.insert(tk.END, "USER ACTIVITY REPORT\n")
        self.report_text.insert(tk.END, "=" * 80 + "\n\n")
        self.report_text.insert(tk.END, f"Generated: {data['generated_at']}\n\n")
        
        # Users
        self.report_text.insert(tk.END, "USERS\n")
        self.report_text.insert(tk.END, "-" * 40 + "\n")
        self.report_text.insert(tk.END, f"{'Username':<15} {'Email':<25} {'Role':<10} {'Created':<20}\n")
        self.report_text.insert(tk.END, "-" * 70 + "\n")
        
        for user in data['users']:
            self.report_text.insert(tk.END, 
                f"{user[1]:<15} {user[2] or 'N/A':<25} {user[3]:<10} {user[4]:<20}\n")

    def _display_supplier_report(self):
        """Display supplier report in text widget"""
        data = self.current_report_data
        
        # Header
        self.report_text.insert(tk.END, "=" * 80 + "\n")
        self.report_text.insert(tk.END, "SUPPLIER REPORT\n")
        self.report_text.insert(tk.END, "=" * 80 + "\n\n")
        self.report_text.insert(tk.END, f"Generated: {data['generated_at']}\n\n")
        
        # Suppliers
        self.report_text.insert(tk.END, "SUPPLIERS\n")
        self.report_text.insert(tk.END, "-" * 40 + "\n")
        self.report_text.insert(tk.END, f"{'Name':<25} {'Contact':<20} {'Phone':<15} {'Email':<25}\n")
        self.report_text.insert(tk.END, "-" * 85 + "\n")
        
        for supplier in data['suppliers']:
            self.report_text.insert(tk.END, 
                f"{supplier[1]:<25} {supplier[2] or 'N/A':<20} {supplier[3] or 'N/A':<15} {supplier[4] or 'N/A':<25}\n")

    def _display_profit_loss_report(self):
        """Display profit and loss report in text widget"""
        data = self.current_report_data
        
        # Header
        self.report_text.insert(tk.END, "=" * 80 + "\n")
        self.report_text.insert(tk.END, "PROFIT AND LOSS REPORT\n")
        self.report_text.insert(tk.END, "=" * 80 + "\n\n")
        self.report_text.insert(tk.END, f"Generated: {data['generated_at']}\n")
        self.report_text.insert(tk.END, f"Period: {data['period_start']} to {data['period_end']}\n\n")
        
        # Summary
        self.report_text.insert(tk.END, "PROFIT & LOSS SUMMARY\n")
        self.report_text.insert(tk.END, "-" * 40 + "\n")
        self.report_text.insert(tk.END, f"{'Total Revenue:':<20} ${data['total_revenue']:>10.2f}\n")
        self.report_text.insert(tk.END, f"{'Total Cost:':<20} ${data['total_cost']:>10.2f}\n")
        self.report_text.insert(tk.END, f"{'Gross Profit:':<20} ${data['gross_profit']:>10.2f}\n")
        self.report_text.insert(tk.END, f"{'Net Profit:':<20} ${data['net_profit']:>10.2f}\n")
        self.report_text.insert(tk.END, f"{'Items Sold:':<20} {data['items_sold']:>10}\n")
        self.report_text.insert(tk.END, f"{'Items Purchased:':<20} {data['items_purchased']:>10}\n")
        
        # Profit indicator
        if data['net_profit'] >= 0:
            self.report_text.insert(tk.END, f"\n{'PROFIT:':<20} ${data['net_profit']:>10.2f}\n")
        else:
            self.report_text.insert(tk.END, f"\n{'LOSS:':<20} ${abs(data['net_profit']):>10.2f}\n")
        
        self.report_text.insert(tk.END, "\n")
        
        # Category breakdown
        if data.get('category_breakdown'):
            self.report_text.insert(tk.END, "CATEGORY BREAKDOWN\n")
            self.report_text.insert(tk.END, "-" * 40 + "\n")
            self.report_text.insert(tk.END, f"{'Category':<20} {'Revenue':<12} {'Cost':<12} {'Profit':<12}\n")
            self.report_text.insert(tk.END, "-" * 60 + "\n")
            
            for cat in data['category_breakdown']:
                revenue = cat[1] or 0.0
                cost = cat[2] or 0.0
                profit = revenue - cost
                self.report_text.insert(tk.END, 
                    f"{cat[0]:<20} ${revenue:>11.2f} ${cost:>11.2f} ${profit:>11.2f}\n")
            
            self.report_text.insert(tk.END, "\n")
        
        # Top profitable items
        if data.get('top_items'):
            self.report_text.insert(tk.END, "TOP PROFITABLE ITEMS\n")
            self.report_text.insert(tk.END, "-" * 40 + "\n")
            self.report_text.insert(tk.END, f"{'Item':<25} {'Category':<15} {'Profit':<12}\n")
            self.report_text.insert(tk.END, "-" * 55 + "\n")
            
            for item in data['top_items'][:10]:  # Top 10 items
                profit = item[4] or 0.0
                self.report_text.insert(tk.END, 
                    f"{item[0]:<25} {item[1]:<15} ${profit:>11.2f}\n")

    def export_report(self, format_type):
        """Export current report"""
        if not self.current_report_data:
            messagebox.showerror("Error", "Please generate a report first!")
            return
        
        try:
            self.set_report_status(f"Exporting to {format_type.upper()}...", 'processing')
            
            # Use built-in export function to avoid import issues
            success, message = self._export_report_builtin(format_type)
            
            if success:
                messagebox.showinfo("Success", message)
                self.set_report_status("✅ Report exported successfully!", 'success')
            else:
                messagebox.showerror("Error", message)
                self.set_report_status("❌ Export failed", 'error')
                
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
            self.set_report_status("❌ Export failed", 'error')

    def _export_report_builtin(self, format_type):
        """Built-in export function that doesn't rely on external utilities"""
        try:
            from tkinter import filedialog
            import csv
            
            # Get filename from user
            if format_type == 'csv':
                filename = filedialog.asksaveasfilename(
                    parent=self.root,
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                )
            else:  # txt
                filename = filedialog.asksaveasfilename(
                    parent=self.root,
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )
                
            if not filename:
                return False, "No file selected"
            
            if format_type == 'csv':
                # Export as CSV using report data
                return self._export_csv_builtin(filename)
            else:
                # Export as text using the displayed content
                with open(filename, 'w', encoding='utf-8') as txtfile:
                    report_content = self.report_text.get(1.0, tk.END)
                    txtfile.write(report_content)
                return True, f"Report exported successfully to {filename}"
                
        except Exception as e:
                return False, f"Error exporting: {str(e)}"

    def _export_csv_builtin(self, filename):
        """Built-in CSV export function"""
        try:
            import csv
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                data = self.current_report_data
                
                # Write header
                writer.writerow(['INVENTORY MANAGEMENT SYSTEM REPORT'])
                writer.writerow(['Generated:', data.get('generated_at', 'N/A')])
                if 'filter_period' in data:
                    writer.writerow(['Period:', data['filter_period']])
                writer.writerow([])
                
                # Write based on report type
                if 'items' in data:  # Inventory Report
                    writer.writerow(['INVENTORY SUMMARY'])
                    writer.writerow(['Total Items:', data['summary']['total_items']])
                    writer.writerow(['Total Quantity:', data['summary']['total_quantity']])
                    writer.writerow(['Total Value:', f"${data['summary']['total_value']:.2f}"])
                    writer.writerow([])
                    
                    writer.writerow(['INVENTORY ITEMS'])
                    writer.writerow(['ID', 'Name', 'Category', 'Quantity', 'Price', 'Total Value', 'Unit', 'Status'])
                    for item in data['items']:
                        writer.writerow([
                            item[0], item[1], item[2], item[3], 
                            f"${item[4]:.2f}", f"${item[5]:.2f}", 
                            item[6] or 'N/A', item[7]
                        ])
                
                elif 'transactions' in data:  # Transaction Report
                    writer.writerow(['TRANSACTION SUMMARY'])
                    for summary in data.get('summary', []):
                        writer.writerow([
                            f"{summary[0].title()}: {summary[1]} transactions, "
                            f"Total quantity: {summary[2]}, Total value: ${summary[3]:.2f}"
                        ])
                    writer.writerow([])
                    
                    writer.writerow(['TRANSACTIONS'])
                    writer.writerow(['ID', 'Date', 'Type', 'Item', 'Category', 'Quantity', 'Unit', 'Value', 'Notes'])
                    for trans in data.get('transactions', []):
                        writer.writerow([
                            trans[0], trans[1], trans[2], trans[5], trans[6],
                            trans[3], trans[7] or 'N/A', f"${trans[8]:.2f}", trans[4] or ''
                        ])
                
                elif 'sales' in data:  # Sales Report
                    writer.writerow(['SALES REPORT'])
                    writer.writerow(['Generated:', data.get('generated_at', 'N/A')])
                    writer.writerow(['Period:', data.get('filter_period', 'All time')])
                    writer.writerow([])
                    
                    writer.writerow(['SALES TRANSACTIONS'])
                    writer.writerow(['Date', 'Item', 'Category', 'Quantity', 'Unit', 'Price', 'Total Value', 'Notes'])
                    for sale in data.get('sales', []):
                        writer.writerow([
                            sale[0], sale[1], sale[2], sale[3], sale[4] or 'N/A',
                            f"${sale[5]:.2f}", f"${sale[6]:.2f}", sale[7] or ''
                        ])
                
                elif 'users' in data:  # User Activity Report
                    writer.writerow(['USER ACTIVITY REPORT'])
                    writer.writerow(['Generated:', data.get('generated_at', 'N/A')])
                    writer.writerow([])
                    
                    writer.writerow(['USERS'])
                    writer.writerow(['ID', 'Username', 'Email', 'Role', 'Created At', 'Transaction Count'])
                    for user in data.get('users', []):
                        writer.writerow([
                            user[0], user[1], user[2] or 'N/A', user[3], user[4], user[5]
                        ])
                
                elif 'suppliers' in data:  # Supplier Report
                    writer.writerow(['SUPPLIER REPORT'])
                    writer.writerow(['Generated:', data.get('generated_at', 'N/A')])
                    writer.writerow([])
                    
                    writer.writerow(['SUPPLIERS'])
                    writer.writerow(['ID', 'Name', 'Contact Person', 'Phone', 'Email', 'Address'])
                    for supplier in data.get('suppliers', []):
                        writer.writerow([
                            supplier[0], supplier[1], supplier[2] or 'N/A',
                            supplier[3] or 'N/A', supplier[4] or 'N/A', supplier[5] or 'N/A'
                        ])
                
                elif 'total_revenue' in data:  # Profit & Loss Report
                    writer.writerow(['PROFIT AND LOSS REPORT'])
                    writer.writerow(['Generated:', data.get('generated_at', 'N/A')])
                    writer.writerow(['Period:', f"{data.get('period_start', 'All time')} to {data.get('period_end', 'All time')}"])
                    writer.writerow([])
                    
                    writer.writerow(['PROFIT & LOSS SUMMARY'])
                    writer.writerow(['Metric', 'Amount'])
                    writer.writerow(['Total Revenue', f"${data.get('total_revenue', 0):.2f}"])
                    writer.writerow(['Total Cost', f"${data.get('total_cost', 0):.2f}"])
                    writer.writerow(['Gross Profit', f"${data.get('gross_profit', 0):.2f}"])
                    writer.writerow(['Net Profit', f"${data.get('net_profit', 0):.2f}"])
                    writer.writerow(['Items Sold', data.get('items_sold', 0)])
                    writer.writerow(['Items Purchased', data.get('items_purchased', 0)])
                    writer.writerow([])
                    
                    if data.get('category_breakdown'):
                        writer.writerow(['CATEGORY BREAKDOWN'])
                        writer.writerow(['Category', 'Revenue', 'Cost', 'Profit'])
                        for cat in data['category_breakdown']:
                            revenue = cat[1] or 0.0
                            cost = cat[2] or 0.0
                            profit = revenue - cost
                            writer.writerow([cat[0], f"${revenue:.2f}", f"${cost:.2f}", f"${profit:.2f}"])
                        writer.writerow([])
                    
                    if data.get('top_items'):
                        writer.writerow(['TOP PROFITABLE ITEMS'])
                        writer.writerow(['Item', 'Category', 'Profit'])
                        for item in data['top_items'][:10]:
                            profit = item[4] or 0.0
                            writer.writerow([item[0], item[1], f"${profit:.2f}"])
            
            return True, f"Report exported successfully to {filename}"
            
        except Exception as e:
            return False, f"Error exporting to CSV: {str(e)}"
