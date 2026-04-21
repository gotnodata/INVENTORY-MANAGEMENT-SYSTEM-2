"""Categories management tab module"""
import tkinter as tk
from tkinter import ttk, messagebox
import config
from database import models
from ui.theme import SearchBar, Tooltip, ValidationFrame, StatusBadge


class CategoriesTab:
    """Categories management tab class"""
    
    def __init__(self, notebook, status_bar_updater):
        self.notebook = notebook
        self.update_status_bar = status_bar_updater
        self.all_categories = []  # Store all categories for filtering
        
        # Create frame and add to notebook
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📂 Categories")
        
        # Create UI
        self.create_ui()
        
        # Load initial data
        self.refresh_categories()
    
    def create_ui(self):
        """Create categories tab UI with enhanced layout"""
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ New Category", command=self._on_new_category, width=18).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_categories, width=15).pack(side=tk.LEFT, padx=2)
        
        # Left panel for form
        left_frame = ttk.LabelFrame(self.frame, text="📝 Category Details", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Name:", font=config.DEFAULT_FONT_LABEL).grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        self.category_name_var = tk.StringVar()
        self.name_entry = ttk.Entry(left_frame, textvariable=self.category_name_var, width=config.ENTRY_FIELD_WIDTH)
        self.name_entry.grid(row=0, column=1, pady=(10, 5))
        self.name_status = ttk.Label(left_frame, text="")
        self.name_status.grid(row=0, column=2, padx=5)
        self.name_entry.bind("<KeyRelease>", lambda e: self._validate_name())
        
        ttk.Label(left_frame, text="Description:", font=config.DEFAULT_FONT_LABEL).grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.category_desc_var = tk.StringVar()
        desc_entry = ttk.Entry(left_frame, textvariable=self.category_desc_var, width=config.ENTRY_FIELD_WIDTH)
        desc_entry.grid(row=1, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="➕ Add", command=self.add_category, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="✏️ Update", command=self.update_category, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_category, width=10).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🔄 Clear", command=self.clear_form, width=10).pack(side=tk.LEFT, padx=3)
        
        # Right panel for list
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="📂 Categories", font=config.DEFAULT_FONT_LABEL).pack(side=tk.LEFT)
        self.category_count_label = ttk.Label(header_frame, text="Categories: 0", font=config.DEFAULT_FONT_BODY)
        self.category_count_label.pack(side=tk.RIGHT)
        
        # Treeview for categories
        columns = ('ID', 'Name', 'Description')
        self.categories_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        self.categories_tree.heading('ID', text='ID')
        self.categories_tree.heading('Name', text='Name')
        self.categories_tree.heading('Description', text='Description')
        
        self.categories_tree.column('ID', width=40, anchor='center')
        self.categories_tree.column('Name', width=120)
        self.categories_tree.column('Description', width=200)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.categories_tree.yview)
        self.categories_tree.configure(yscrollcommand=scrollbar.set)
        
        self.categories_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.categories_tree.bind('<Double-1>', self.on_double_click)
        self.categories_tree.bind('<Button-3>', self._show_context_menu)
        
        # Context menu
        self.context_menu = tk.Menu(self.categories_tree, tearoff=0)
        self.context_menu.add_command(label="✎ Edit", command=self._context_edit)
        self.context_menu.add_command(label="🗑️ Delete", command=self._context_delete)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy ID", command=self._context_copy_id)
    
    def _validate_name(self):
        """Real-time validation for name"""
        value = self.category_name_var.get().strip()
        if value:
            self.name_status.config(text="✓", foreground=config.COLOR_SUCCESS)
        else:
            self.name_status.config(text="✗", foreground=config.COLOR_DANGER)
    
    def _on_new_category(self):
        """Handle new category"""
        self.clear_form()
        self.name_entry.focus()
        self.update_status_bar("✎ Ready to add new category")
    
    def _on_search_change(self, search_term):
        """Handle search input change"""
        if not search_term:
            self.refresh_categories()
            return
        
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        search_term = search_term.lower()
        for category in self.all_categories:
            cat_id, name, description = category
            
            if (search_term in str(name).lower() or 
                search_term in str(description).lower() or
                search_term in str(cat_id)):
                
                self.categories_tree.insert('', 'end', values=category)
        
        self.category_count_label.config(text=f"Categories: {len(self.categories_tree.get_children())}")
    
    def _show_context_menu(self, event):
        """Show right-click context menu"""
        item = self.categories_tree.selection()
        if item:
            self.categories_tree.selection_set(item)
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def _context_edit(self):
        """Context menu: Edit category"""
        self.on_double_click(None)
    
    def _context_delete(self):
        """Context menu: Delete category"""
        self.delete_category()
    
    def _context_copy_id(self):
        """Context menu: Copy category ID"""
        selected = self.categories_tree.selection()
        if selected:
            cat_id = self.categories_tree.item(selected[0])['values'][0]
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(cat_id))
            self.update_status_bar(f"📋 Category ID {cat_id} copied to clipboard")
    
    def add_category(self):
        """Add a new category"""
        name = self.category_name_var.get().strip()
        description = self.category_desc_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Category name is required!")
            self.name_entry.focus()
            return
            
        models.add_category(name, description)
        self.clear_form()
        self.refresh_categories()
        self.update_status_bar(f"✓ Category '{name}' added successfully!")
        
    def update_category(self):
        """Update selected category"""
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to update!")
            return
            
        category_id = self.categories_tree.item(selected[0])['values'][0]
        name = self.category_name_var.get().strip() or None
        description = self.category_desc_var.get().strip() or None
        
        models.update_category(category_id, name, description)
        self.clear_form()
        self.refresh_categories()
        self.update_status_bar(f"✓ Category ID {category_id} updated successfully!")
        
    def delete_category(self):
        """Delete selected category"""
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to delete!")
            return
        
        cat_values = self.categories_tree.item(selected[0])['values']
        category_id = cat_values[0]
        category_name = cat_values[1]
            
        if messagebox.askyesno("Confirm Delete", f"Delete '{category_name}'? This cannot be undone."):
            models.delete_category(category_id)
            self.clear_form()
            self.refresh_categories()
            self.update_status_bar(f"✓ Category '{category_name}' deleted successfully!")
    
    def clear_form(self):
        """Clear category form fields"""
        self.category_name_var.set("")
        self.category_desc_var.set("")
        self.name_status.config(text="")
    
    def refresh_categories(self):
        """Refresh categories display"""
        # Clear existing categories
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
            
        categories = models.get_categories()
        self.all_categories = categories
        
        for category in categories:
            self.categories_tree.insert('', 'end', values=category)
        
        self.category_count_label.config(text=f"Categories: {len(self.categories_tree.get_children())}")
    
    def on_double_click(self, event):
        """Handle double click on category"""
        selected = self.categories_tree.selection()
        if selected:
            category = self.categories_tree.item(selected[0])['values']
            self.category_name_var.set(category[1])
            self.category_desc_var.set(category[2])
