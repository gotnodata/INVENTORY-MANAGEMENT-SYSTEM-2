"""Suppliers management tab module"""
import tkinter as tk
from tkinter import ttk, messagebox
import config
from database import models
from database.models.suppliers import *


class SuppliersTab:
    """Suppliers management tab class"""
    
    def __init__(self, notebook, status_bar_updater):
        self.notebook = notebook
        self.update_status_bar = status_bar_updater
        self.all_suppliers = []  # Store all suppliers for filtering
        
        # Create frame and add to notebook
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🏭 Suppliers")
        
        # Create UI
        self.create_ui()
        
        # Load initial data
        self.refresh_suppliers()
    
    def create_ui(self):
        """Create suppliers tab UI with enhanced layout"""
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ New Supplier", command=self._on_new_supplier, width=18).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_suppliers, width=15).pack(side=tk.LEFT, padx=2)
        
        # Left panel for form
        left_frame = ttk.LabelFrame(self.frame, text="📝 Supplier Details", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Name:", font=config.DEFAULT_FONT_LABEL).grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        self.supplier_name_var = tk.StringVar()
        self.name_entry = ttk.Entry(left_frame, textvariable=self.supplier_name_var, width=config.ENTRY_FIELD_WIDTH)
        self.name_entry.grid(row=0, column=1, pady=(10, 5))
        
        ttk.Label(left_frame, text="Contact:", font=config.DEFAULT_FONT_LABEL).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.supplier_contact_var = tk.StringVar()
        self.contact_entry = ttk.Entry(left_frame, textvariable=self.supplier_contact_var, width=config.ENTRY_FIELD_WIDTH)
        self.contact_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(left_frame, text="Email:", font=config.DEFAULT_FONT_LABEL).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.supplier_email_var = tk.StringVar()
        self.email_entry = ttk.Entry(left_frame, textvariable=self.supplier_email_var, width=config.ENTRY_FIELD_WIDTH)
        self.email_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(left_frame, text="Phone:", font=config.DEFAULT_FONT_LABEL).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.supplier_phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(left_frame, textvariable=self.supplier_phone_var, width=config.ENTRY_FIELD_WIDTH)
        self.phone_entry.grid(row=3, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="➕ Add", command=self.add_supplier, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="✏️ Update", command=self.update_supplier, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_supplier, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🔄 Clear", command=self.clear_form, width=10).pack(side=tk.LEFT, padx=3)
        
        # Right panel for list
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="🏭 Suppliers", font=config.DEFAULT_FONT_LABEL).pack(side=tk.LEFT)
        self.supplier_count_label = ttk.Label(header_frame, text="Suppliers: 0", font=config.DEFAULT_FONT_BODY)
        self.supplier_count_label.pack(side=tk.RIGHT)
        
        # Treeview for suppliers
        columns = ('ID', 'Name', 'Contact', 'Email', 'Phone')
        self.suppliers_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        self.suppliers_tree.heading('ID', text='ID')
        self.suppliers_tree.heading('Name', text='Name')
        self.suppliers_tree.heading('Contact', text='Contact')
        self.suppliers_tree.heading('Email', text='Email')
        self.suppliers_tree.heading('Phone', text='Phone')
        
        self.suppliers_tree.column('ID', width=40, anchor='center')
        self.suppliers_tree.column('Name', width=120)
        self.suppliers_tree.column('Contact', width=100)
        self.suppliers_tree.column('Email', width=150)
        self.suppliers_tree.column('Phone', width=100)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.suppliers_tree.yview)
        self.suppliers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.suppliers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.suppliers_tree.bind('<Double-1>', self.on_double_click)
        self.suppliers_tree.bind('<Button-3>', self._show_context_menu)
        
        # Context menu
        self.context_menu = tk.Menu(self.suppliers_tree, tearoff=0)
        self.context_menu.add_command(label="✎ Edit", command=self._context_edit)
        self.context_menu.add_command(label="🗑️ Delete", command=self._context_delete)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy ID", command=self._context_copy_id)
    
    def _on_new_supplier(self):
        """Handle new supplier"""
        self.clear_form()
        self.name_entry.focus()
        self.update_status_bar("✎ Ready to add new supplier")
    
    def _on_search_change(self, search_term):
        """Handle search input change"""
        if not search_term:
            self.refresh_suppliers()
            return
        
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        search_term = search_term.lower()
        for supplier in self.all_suppliers:
            supplier_id, name, contact, email, phone = supplier
            
            if (search_term in str(name).lower() or 
                search_term in str(contact).lower() or
                search_term in str(email).lower() or
                search_term in str(phone).lower() or
                search_term in str(supplier_id)):
                
                self.suppliers_tree.insert('', 'end', values=supplier)
        
        self.supplier_count_label.config(text=f"Suppliers: {len(self.suppliers_tree.get_children())}")
    
    def _show_context_menu(self, event):
        """Show right-click context menu"""
        item = self.suppliers_tree.selection()
        if item:
            self.suppliers_tree.selection_set(item)
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def _context_edit(self):
        """Context menu: Edit supplier"""
        self.on_double_click(None)
    
    def _context_delete(self):
        """Context menu: Delete supplier"""
        self.delete_supplier()
    
    def _context_copy_id(self):
        """Context menu: Copy supplier ID"""
        selected = self.suppliers_tree.selection()
        if selected:
            supplier_id = self.suppliers_tree.item(selected[0])['values'][0]
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(supplier_id))
            self.update_status_bar(f"📋 Supplier ID {supplier_id} copied to clipboard")
    
    def add_supplier(self):
        """Add a new supplier"""
        name = self.supplier_name_var.get().strip()
        contact = self.supplier_contact_var.get().strip()
        email = self.supplier_email_var.get().strip()
        phone = self.supplier_phone_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Supplier name is required!")
            self.name_entry.focus()
            return
            
        models.add_supplier(name, contact, email, phone)
        self.clear_form()
        self.refresh_suppliers()
        self.update_status_bar(f"✓ Supplier '{name}' added successfully!")
        
    def update_supplier(self):
        """Update selected supplier"""
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to update!")
            return
            
        supplier_id = self.suppliers_tree.item(selected[0])['values'][0]
        name = self.supplier_name_var.get().strip() or None
        contact = self.supplier_contact_var.get().strip() or None
        email = self.supplier_email_var.get().strip() or None
        phone = self.supplier_phone_var.get().strip() or None
        
        models.update_supplier(supplier_id, name, contact, email, phone)
        self.clear_form()
        self.refresh_suppliers()
        self.update_status_bar(f"✓ Supplier ID {supplier_id} updated successfully!")
        
    def delete_supplier(self):
        """Delete selected supplier"""
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to delete!")
            return
            
        supplier_values = self.suppliers_tree.item(selected[0])['values']
        supplier_id = supplier_values[0]
        supplier_name = supplier_values[1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete '{supplier_name}'? This cannot be undone."):
            models.delete_supplier(supplier_id)
            self.clear_form()
            self.refresh_suppliers()
            self.update_status_bar(f"✓ Supplier '{supplier_name}' deleted successfully!")
    
    def clear_form(self):
        """Clear supplier form fields"""
        self.supplier_name_var.set("")
        self.supplier_contact_var.set("")
        self.supplier_email_var.set("")
        self.supplier_phone_var.set("")
    
    def refresh_suppliers(self):
        """Refresh suppliers display"""
        # Clear existing suppliers
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
            
        suppliers = models.get_suppliers()
        self.all_suppliers = suppliers
        
        for supplier in suppliers:
            self.suppliers_tree.insert('', 'end', values=supplier)
        
        self.supplier_count_label.config(text=f"Suppliers: {len(self.suppliers_tree.get_children())}")
    
    def on_double_click(self, event):
        """Handle double click on supplier"""
        selected = self.suppliers_tree.selection()
        if selected:
            supplier = self.suppliers_tree.item(selected[0])['values']
            self.supplier_name_var.set(supplier[1])
            self.supplier_contact_var.set(supplier[2])
            self.supplier_email_var.set(supplier[3])
            self.supplier_phone_var.set(supplier[4])
