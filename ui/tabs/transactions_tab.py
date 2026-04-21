"""Transactions management tab module"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import config
from database import models
from database.models.transactions import *


class TransactionsTab:
    """Transactions management tab class"""
    
    def __init__(self, notebook, status_bar_updater):
        self.notebook = notebook
        self.update_status_bar = status_bar_updater
        self.all_transactions = []  # Store all transactions for filtering
        
        # Create frame and add to notebook
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="💳 Transactions")
        
        # Create UI
        self.create_ui()
        
        # Load initial data
        self.refresh_transactions()
    
    def create_ui(self):
        """Create transactions tab UI with enhanced layout"""
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ New Transaction", command=self._on_new_transaction, width=18).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_transactions, width=15).pack(side=tk.LEFT, padx=2)
        
        # Left panel for form
        left_frame = ttk.LabelFrame(self.frame, text="📝 Transaction Details", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Item:", font=config.DEFAULT_FONT_LABEL).grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        self.transaction_item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(left_frame, textvariable=self.transaction_item_var, width=config.ENTRY_FIELD_WIDTH)
        self.item_combo.grid(row=0, column=1, pady=(10, 5))
        self.item_combo.bind('<<ComboboxSelected>>', self.on_item_selected)
        
        ttk.Label(left_frame, text="Type:", font=config.DEFAULT_FONT_LABEL).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.transaction_type_var = tk.StringVar()
        type_combo = ttk.Combobox(left_frame, textvariable=self.transaction_type_var, width=config.ENTRY_FIELD_WIDTH, 
                                 values=[config.TRANSACTION_TYPE_IN, config.TRANSACTION_TYPE_OUT])
        type_combo.grid(row=1, column=1, pady=5)
        type_combo.bind('<<ComboboxSelected>>', self.on_type_changed)
        
        ttk.Label(left_frame, text="Quantity:", font=config.DEFAULT_FONT_LABEL).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.transaction_quantity_var = tk.StringVar()
        self.quantity_entry = ttk.Entry(left_frame, textvariable=self.transaction_quantity_var, width=config.ENTRY_FIELD_WIDTH)
        self.quantity_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(left_frame, text="Date:", font=config.DEFAULT_FONT_LABEL).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.transaction_date_var = tk.StringVar()
        self.transaction_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = ttk.Entry(left_frame, textvariable=self.transaction_date_var, width=config.ENTRY_FIELD_WIDTH)
        self.date_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(left_frame, text="Selling Price:", font=config.DEFAULT_FONT_LABEL).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.transaction_selling_price_var = tk.StringVar()
        self.selling_price_entry = ttk.Entry(left_frame, textvariable=self.transaction_selling_price_var, width=config.ENTRY_FIELD_WIDTH)
        self.selling_price_entry.grid(row=4, column=1, pady=5)
        
        ttk.Label(left_frame, text="Notes:", font=config.DEFAULT_FONT_LABEL).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.transaction_notes_var = tk.StringVar()
        self.notes_entry = ttk.Entry(left_frame, textvariable=self.transaction_notes_var, width=config.ENTRY_FIELD_WIDTH)
        self.notes_entry.grid(row=5, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="➕ Add", command=self.add_transaction, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🔄 Clear", command=self.clear_form, width=10).pack(side=tk.LEFT, padx=3)
        
        # Right panel for list
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="💳 Transactions", font=config.DEFAULT_FONT_LABEL).pack(side=tk.LEFT)
        self.transaction_count_label = ttk.Label(header_frame, text="Transactions: 0", font=config.DEFAULT_FONT_BODY)
        self.transaction_count_label.pack(side=tk.RIGHT)
        
        # Treeview for transactions
        columns = ('ID', 'Item', 'Type', 'Quantity', 'Date', 'Notes')
        self.transactions_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        self.transactions_tree.heading('ID', text='ID')
        self.transactions_tree.heading('Item', text='Item')
        self.transactions_tree.heading('Type', text='Type')
        self.transactions_tree.heading('Quantity', text='Quantity')
        self.transactions_tree.heading('Date', text='Date')
        self.transactions_tree.heading('Notes', text='Notes')
        
        self.transactions_tree.column('ID', width=40, anchor='center')
        self.transactions_tree.column('Item', width=120)
        self.transactions_tree.column('Type', width=60, anchor='center')
        self.transactions_tree.column('Quantity', width=60, anchor='center')
        self.transactions_tree.column('Date', width=80, anchor='center')
        self.transactions_tree.column('Notes', width=150)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.transactions_tree.bind('<Double-1>', self.on_double_click)
        self.transactions_tree.bind('<Button-3>', self._show_context_menu)
        
        # Context menu
        self.context_menu = tk.Menu(self.transactions_tree, tearoff=0)
        self.context_menu.add_command(label="📋 Copy ID", command=self._context_copy_id)
    
    def _on_new_transaction(self):
        """Handle new transaction"""
        self.clear_form()
        self.item_combo.focus()
        self.update_status_bar("✎ Ready to add new transaction")
    
    def _on_search_change(self, search_term):
        """Handle search input change"""
        if not search_term:
            self.refresh_transactions()
            return
        
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        search_term = search_term.lower()
        for transaction in self.all_transactions:
            trans_id, item_name, trans_type, quantity, date, notes = transaction
            
            if (search_term in str(item_name).lower() or 
                search_term in str(trans_type).lower() or
                search_term in str(date).lower() or
                search_term in str(notes).lower() or
                search_term in str(trans_id)):
                
                self.transactions_tree.insert('', 'end', values=transaction)
        
        self.transaction_count_label.config(text=f"Transactions: {len(self.transactions_tree.get_children())}")
    
    def _show_context_menu(self, event):
        """Show right-click context menu"""
        item = self.transactions_tree.selection()
        if item:
            self.transactions_tree.selection_set(item)
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def _context_copy_id(self):
        """Context menu: Copy transaction ID"""
        selected = self.transactions_tree.selection()
        if selected:
            trans_id = self.transactions_tree.item(selected[0])['values'][0]
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(trans_id))
            self.update_status_bar(f"📋 Transaction ID {trans_id} copied to clipboard")
    
    def on_item_selected(self, event):
        """Handle item selection change"""
        item_name = self.transaction_item_var.get()
        if item_name:
            # Update current quantity display
            items = models.view_items()
            for item in items:
                if item[1] == item_name:
                    current_quantity = item[3]
                    self.update_status_bar(f"📊 Current stock: {current_quantity} units")
                    break
    
    def on_type_changed(self, event):
        """Handle transaction type change"""
        trans_type = self.transaction_type_var.get()
        if trans_type == config.TRANSACTION_TYPE_IN:
            # Disable selling price for IN transactions
            self.selling_price_entry.config(state='disabled')
            self.transaction_selling_price_var.set("")
        else:
            # Enable selling price for OUT transactions
            self.selling_price_entry.config(state='normal')
    
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
                
            # Add transaction
            success, message = models.add_transaction(item_id, trans_type, quantity, date, notes, selling_price)
            
            if success:
                self.clear_form()
                self.refresh_transactions()
                
                # Update current quantity display if item is still selected
                if self.transaction_item_var.get() == item_name:
                    items = models.view_items()
                    for item in items:
                        if item[1] == item_name:
                            current_quantity = item[3]
                            self.update_status_bar(f"📊 Current stock: {current_quantity} units")
                            break
                
                self.update_status_bar(f"✓ Transaction added successfully! {message}")
            else:
                messagebox.showerror("Error", message)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid quantity! {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaction: {e}")
    
    def clear_form(self):
        """Clear transaction form fields"""
        self.transaction_item_var.set("")
        self.transaction_type_var.set("")
        self.transaction_quantity_var.set("")
        self.transaction_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.transaction_selling_price_var.set("")
        self.transaction_notes_var.set("")
        # Enable selling price field by default
        self.selling_price_entry.config(state='normal')
        self.update_status_bar("📝 Form cleared")
    
    def refresh_transactions(self):
        """Refresh transactions display"""
        # Clear existing transactions
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
            
        transactions = models.get_transactions()
        self.all_transactions = transactions
        
        for transaction in transactions:
            self.transactions_tree.insert('', 'end', values=transaction)
        
        self.transaction_count_label.config(text=f"Transactions: {len(self.transactions_tree.get_children())}")
        
        # Update items combo
        items = models.view_items()
        item_names = [item[1] for item in items]
        self.item_combo['values'] = item_names
    
    def on_double_click(self, event):
        """Handle double click on transaction"""
        selected = self.transactions_tree.selection()
        if selected:
            transaction = self.transactions_tree.item(selected[0])['values']
            # For transactions, we don't allow editing, just show details
            messagebox.showinfo("Transaction Details", 
                f"ID: {transaction[0]}\n"
                f"Item: {transaction[1]}\n"
                f"Type: {transaction[2]}\n"
                f"Quantity: {transaction[3]}\n"
                f"Date: {transaction[4]}\n"
                f"Notes: {transaction[5]}")
