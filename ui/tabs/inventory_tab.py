"""Inventory management tab module"""
import tkinter as tk
from tkinter import ttk, messagebox
import config
from database import models
from ui.theme import SearchBar, Tooltip, ValidationFrame, StatusBadge


class InventoryTab:
    """Inventory management tab class"""
    
    def __init__(self, notebook, status_bar_updater):
        self.notebook = notebook
        self.update_status_bar = status_bar_updater
        self.all_items = []  # Store all items for filtering
        
        # Create frame and add to notebook
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📦 Inventory")
        
        # Create UI
        self.create_ui()
        
        # Load initial data
        self.refresh_inventory()
    
    def create_ui(self):
        """Create inventory tab UI with enhanced layout"""
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ New Item", command=self._on_new_item, width=18).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_inventory, width=15).pack(side=tk.LEFT, padx=2)
        
        # Left panel for form
        left_frame = ttk.LabelFrame(self.frame, text="📝 Item Details", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Name:", font=config.DEFAULT_FONT_LABEL).grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        self.item_name_var = tk.StringVar()
        self.name_entry = ttk.Entry(left_frame, textvariable=self.item_name_var, width=config.ENTRY_FIELD_WIDTH)
        self.name_entry.grid(row=0, column=1, pady=(10, 5))
        self.name_status = ttk.Label(left_frame, text="")
        self.name_status.grid(row=0, column=2, padx=5)
        self.name_entry.bind("<KeyRelease>", lambda e: self._validate_name())
        
        ttk.Label(left_frame, text="Category:", font=config.DEFAULT_FONT_LABEL).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.item_category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(left_frame, textvariable=self.item_category_var, width=config.ENTRY_FIELD_WIDTH)
        self.category_combo.grid(row=1, column=1, pady=5)
        
        ttk.Label(left_frame, text="Quantity:", font=config.DEFAULT_FONT_LABEL).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.item_quantity_var = tk.StringVar()
        self.quantity_entry = ttk.Entry(left_frame, textvariable=self.item_quantity_var, width=config.ENTRY_FIELD_WIDTH)
        self.quantity_entry.grid(row=2, column=1, pady=5)
        self.quantity_status = ttk.Label(left_frame, text="")
        self.quantity_status.grid(row=2, column=2, padx=5)
        self.quantity_entry.bind("<KeyRelease>", lambda e: self._validate_quantity())
        
        ttk.Label(left_frame, text="Cost Price:", font=config.DEFAULT_FONT_LABEL).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.item_cost_price_var = tk.StringVar()
        self.cost_price_entry = ttk.Entry(left_frame, textvariable=self.item_cost_price_var, width=config.ENTRY_FIELD_WIDTH)
        self.cost_price_entry.grid(row=3, column=1, pady=5)
        self.cost_price_status = ttk.Label(left_frame, text="")
        self.cost_price_status.grid(row=3, column=2, padx=5)
        self.cost_price_entry.bind("<KeyRelease>", lambda e: self._validate_cost_price())
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="➕ Add", command=self.add_item, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="✏️ Update", command=self.update_item, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_item, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🔄 Clear", command=self.clear_form, width=10).pack(side=tk.LEFT, padx=3)
        
        # Right panel for list
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="📦 Inventory Items", font=config.DEFAULT_FONT_LABEL).pack(side=tk.LEFT)
        self.item_count_label = ttk.Label(header_frame, text="Items: 0", font=config.DEFAULT_FONT_BODY)
        self.item_count_label.pack(side=tk.RIGHT)
        
        # Treeview for inventory
        columns = ('ID', 'Name', 'Category', 'Quantity', 'Cost Price')
        self.inventory_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        self.inventory_tree.heading('ID', text='ID')
        self.inventory_tree.heading('Name', text='Name')
        self.inventory_tree.heading('Category', text='Category')
        self.inventory_tree.heading('Quantity', text='Quantity')
        self.inventory_tree.heading('Cost Price', text='Cost Price')
        
        self.inventory_tree.column('ID', width=40, anchor='center')
        self.inventory_tree.column('Name', width=150)
        self.inventory_tree.column('Category', width=120)
        self.inventory_tree.column('Quantity', width=80, anchor='center')
        self.inventory_tree.column('Cost Price', width=100, anchor='e')
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        self.inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.inventory_tree.bind('<Double-1>', self.on_double_click)
        self.inventory_tree.bind('<Button-3>', self._show_context_menu)
        
        # Context menu
        self.context_menu = tk.Menu(self.inventory_tree, tearoff=0)
        self.context_menu.add_command(label="✎ Edit", command=self._context_edit)
        self.context_menu.add_command(label="🗑️ Delete", command=self._context_delete)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy ID", command=self._context_copy_id)
    
    def _validate_name(self):
        """Real-time validation for name"""
        value = self.item_name_var.get().strip()
        if value:
            self.name_status.config(text="✓", foreground=config.COLOR_SUCCESS)
        else:
            self.name_status.config(text="✗", foreground=config.COLOR_DANGER)
    
    def _validate_quantity(self):
        """Real-time validation for quantity"""
        value = self.item_quantity_var.get().strip()
        try:
            if value and int(value) >= 0:
                self.quantity_status.config(text="✓", foreground=config.COLOR_SUCCESS)
            else:
                self.quantity_status.config(text="✗", foreground=config.COLOR_DANGER)
        except ValueError:
            self.quantity_status.config(text="✗", foreground=config.COLOR_DANGER)
    
    def _validate_cost_price(self):
        """Real-time validation for cost price"""
        value = self.item_cost_price_var.get().strip()
        try:
            if value and float(value) >= 0:
                self.cost_price_status.config(text="✓", foreground=config.COLOR_SUCCESS)
            else:
                self.cost_price_status.config(text="✗", foreground=config.COLOR_DANGER)
        except ValueError:
            self.cost_price_status.config(text="✗", foreground=config.COLOR_DANGER)
    
    def _on_new_item(self):
        """Handle new item"""
        self.clear_form()
        self.name_entry.focus()
        self.update_status_bar("✎ Ready to add new item")
    
    def _show_context_menu(self, event):
        """Show right-click context menu"""
        item = self.inventory_tree.selection()
        if item:
            self.inventory_tree.selection_set(item)
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def _context_edit(self):
        """Context menu: Edit item"""
        self.on_double_click(None)
    
    def _context_delete(self):
        """Context menu: Delete item"""
        self.delete_item()
    
    def _context_copy_id(self):
        """Context menu: Copy item ID"""
        selected = self.inventory_tree.selection()
        if selected:
            item_id = self.inventory_tree.item(selected[0])['values'][0]
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(item_id))
            self.update_status_bar(f"📋 Item ID {item_id} copied to clipboard")
    
    def add_item(self):
        """Add a new inventory item"""
        try:
            name = self.item_name_var.get().strip()
            category_name = self.item_category_var.get().strip()
            quantity = int(self.item_quantity_var.get())
            cost_price = float(self.item_cost_price_var.get())
            
            if not name:
                messagebox.showerror("Error", "Item name is required!")
                self.name_entry.focus()
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
            self.clear_form()
            self.refresh_inventory()
            self.update_status_bar(f"✓ Item '{name}' added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or cost price!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")
    
    def update_item(self):
        """Update selected inventory item"""
        try:
            selected = self.inventory_tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select an item to update!")
                return
                
            item_id = self.inventory_tree.item(selected[0])['values'][0]
            name = self.item_name_var.get().strip() or None
            category_name = self.item_category_var.get().strip() or None
            quantity = int(self.item_quantity_var.get()) if self.item_quantity_var.get() else None
            cost_price = float(self.item_cost_price_var.get()) if self.item_cost_price_var.get() else None
            
            # Get category ID if category provided
            category_id = None
            if category_name:
                categories = models.get_categories()
                for cat in categories:
                    if cat[1] == category_name:
                        category_id = cat[0]
                        break
            
            models.update_item(item_id, name, category_id, quantity, cost_price)
            self.clear_form()
            self.refresh_inventory()
            self.update_status_bar(f"✓ Item ID {item_id} updated successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or cost price!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {e}")
    
    def delete_item(self):
        """Delete selected inventory item"""
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to delete!")
            return
            
        item_values = self.inventory_tree.item(selected[0])['values']
        item_id = item_values[0]
        item_name = item_values[1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete '{item_name}'? This cannot be undone."):
            models.delete_item(item_id)
            self.clear_form()
            self.refresh_inventory()
            self.update_status_bar(f"✓ Item '{item_name}' deleted successfully!")
    
    def clear_form(self):
        """Clear inventory form fields"""
        self.item_name_var.set("")
        self.item_category_var.set("")
        self.item_quantity_var.set("")
        self.item_cost_price_var.set("")
        
        # Clear validation status
        self.name_status.config(text="")
        self.quantity_status.config(text="")
        self.cost_price_status.config(text="")
    
    def refresh_inventory(self):
        """Refresh inventory display"""
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
            
        items = models.view_items()
        self.all_items = []
        
        for item in items:
            # Data structure from SELECT i.*, c.name, mu.unit_name, mu.unit_symbol:
            # [id, name, category_id, quantity, price, measurement_unit_id, category_name, unit_name, unit_symbol, cost_price]
            
            # Extract values with correct indices
            item_id = item[0]
            item_name = item[1]
            category_name = item[6] if item[6] else "No Category"  # category_name at index 6
            quantity = item[3]
            unit_symbol = item[8] if item[8] else ""  # unit_symbol at index 8
            cost_price = item[9] if len(item) > 9 else 0.0  # cost_price at index 9
            
            # Store for search functionality
            self.all_items.append([item_id, item_name, category_name, quantity, cost_price])
            
            # Create display values: [id, name, category_name, quantity_with_unit, cost_price]
            display_values = [
                item_id,  # ID
                item_name,  # Name
                category_name,  # Category name
                f"{quantity} {unit_symbol}" if unit_symbol else str(quantity),  # Quantity with unit
                cost_price  # Cost Price
            ]
            self.inventory_tree.insert('', 'end', values=display_values)
        
        self.item_count_label.config(text=f"Items: {len(self.inventory_tree.get_children())}")
        
        # Update categories combo
        categories = models.get_categories()
        category_names = [cat[1] for cat in categories]
        self.category_combo['values'] = category_names
    
    def on_double_click(self, event):
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
